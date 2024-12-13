package se.kth.jabeja;

import org.apache.log4j.Logger;
import se.kth.jabeja.config.Config;
import se.kth.jabeja.config.NodeSelectionPolicy;
import se.kth.jabeja.io.FileIO;
import se.kth.jabeja.rand.RandNoGenerator;

import java.io.File;
import java.io.IOException;
import java.util.*;

public class Jabeja {
    final static Logger logger = Logger.getLogger(Jabeja.class);
    private final Config config;
    private final HashMap<Integer, Node> entireGraph;
    private final List<Integer> nodeIds;
    private int numberOfSwaps;
    private int round;
    private float T;
    private boolean resultFileCreated = false;

    public Jabeja(HashMap<Integer, Node> graph, Config config) {
        this.entireGraph = graph;
        this.nodeIds = new ArrayList<>(entireGraph.keySet());
        this.round = 0;
        this.numberOfSwaps = 0;
        this.config = config;
        this.T = config.getTemperature();
    }

    public void startJabeja() throws IOException {
        for (round = 0; round < config.getRounds(); round++) {
            for (int id : entireGraph.keySet()) {
                sampleAndSwap(id);
            }

            saCoolDown();
            report();
        }
    }

    private void saCoolDown() {
        if (T > 1) T -= config.getDelta();
        if (T < 1) T = 1;
    }

    private void sampleAndSwap(int nodeId) {
        Node nodep = entireGraph.get(nodeId);
        Node partner = null;

        if (config.getNodeSelectionPolicy() == NodeSelectionPolicy.LOCAL || 
            config.getNodeSelectionPolicy() == NodeSelectionPolicy.HYBRID) {
            Integer[] neighbors = getNeighbors(nodep);
            partner = findPartner(nodeId, neighbors);
        }

        if ((partner == null) && 
            (config.getNodeSelectionPolicy() == NodeSelectionPolicy.RANDOM || 
            config.getNodeSelectionPolicy() == NodeSelectionPolicy.HYBRID)) {
            Integer[] randomSample = getSample(nodeId);
            partner = findPartner(nodeId, randomSample);
        }

        if (partner != null) {
            int tempColor = nodep.getColor();
            nodep.setColor(partner.getColor());
            partner.setColor(tempColor);
            numberOfSwaps++;
        }
    }

    public Node findPartner(int nodeId, Integer[] candidates) {
        Node nodep = entireGraph.get(nodeId);
        Node bestPartner = null;
        double highestBenefit = 0;

        for (int candidateId : candidates) {
            Node candidate = entireGraph.get(candidateId);

            if (candidate == null || nodep.getColor() == candidate.getColor()) {
                continue;
            }

            double currentBenefit = Math.pow(getDegree(nodep, nodep.getColor()), config.getAlpha()) +
                                    Math.pow(getDegree(candidate, candidate.getColor()), config.getAlpha());
            double newBenefit = Math.pow(getDegree(nodep, candidate.getColor()), config.getAlpha()) +
                                Math.pow(getDegree(candidate, nodep.getColor()), config.getAlpha());

            if (newBenefit * T > currentBenefit && newBenefit > highestBenefit) {
                bestPartner = candidate;
                highestBenefit = newBenefit;
            }
        }
        return bestPartner;
    }

    private int getDegree(Node node, int colorId) {
        int degree = 0;
        for (int neighborId : node.getNeighbours()) {
            Node neighbor = entireGraph.get(neighborId);
            if (neighbor.getColor() == colorId) {
                degree++;
            }
        }
        return degree;
    }

    private Integer[] getSample(int currentNodeId) {
        int count = config.getUniformRandomSampleSize();
        ArrayList<Integer> rndIds = new ArrayList<>();
        while (rndIds.size() < count) {
            int rndId = nodeIds.get(RandNoGenerator.nextInt(entireGraph.size()));
            if (rndId != currentNodeId && !rndIds.contains(rndId)) {
                rndIds.add(rndId);
            }
        }
        return rndIds.toArray(new Integer[0]);
    }

    private Integer[] getNeighbors(Node node) {
        ArrayList<Integer> list = node.getNeighbours();
        ArrayList<Integer> rndIds = new ArrayList<>();
        int count = Math.min(config.getRandomNeighborSampleSize(), list.size());

        while (rndIds.size() < count) {
            int rndId = list.get(RandNoGenerator.nextInt(list.size()));
            if (!rndIds.contains(rndId)) {
                rndIds.add(rndId);
            }
        }
        return rndIds.toArray(new Integer[0]);
    }

    private void report() throws IOException {
        int grayLinks = 0, migrations = 0;

        for (Node node : entireGraph.values()) {
            if (node.getColor() != node.getInitColor()) migrations++;
            for (int neighborId : node.getNeighbours()) {
                Node neighbor = entireGraph.get(neighborId);
                if (node.getColor() != neighbor.getColor()) grayLinks++;
            }
        }

        int edgeCut = grayLinks / 2;
        logger.info("round: " + round + ", edge cut: " + edgeCut + ", swaps: " + numberOfSwaps + ", migrations: " + migrations);
        saveToFile(edgeCut, migrations);
    }

    private void saveToFile(int edgeCuts, int migrations) throws IOException {
        String delimiter = "\t";
        File inputFile = new File(config.getGraphFilePath());
        String outputFilePath = config.getOutputDir() + File.separator + inputFile.getName() + ".txt";

        if (!resultFileCreated) {
            File outputDir = new File(config.getOutputDir());
            if (!outputDir.exists() && !outputDir.mkdir()) {
                throw new IOException("Unable to create the output directory.");
            }
            String header = "Round" + delimiter + "Edge-Cut" + delimiter + "Swaps" + delimiter + "Migrations\n";
            FileIO.write(header, outputFilePath);
            resultFileCreated = true;
        }

        String line = round + delimiter + edgeCuts + delimiter + numberOfSwaps + delimiter + migrations + "\n";
        FileIO.append(line, outputFilePath);
    }
}
