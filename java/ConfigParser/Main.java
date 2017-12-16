

public class Main {
    public static void main(String[] args) {
        if (args.length <= 0) {
          System.out.println("Command: java CrfTrainer " +
          "--train=trainingDateFile " +
          "--model=generatedModelFile " +
          "--template=templateFile " +
          "--crf_so_loc= path to your crf .so files " +
          "--f = ngram frequency " +
          "--c = learning regularization parameter"
          );
          System.exit(1);
        }


        ConfigParser config = new ConfigParser(args);
        config.checkRequiredArgs(new String[] { "train", "model", "template","crf_so_loc",
            "log_properties"});

        String soDir = config.getOption("crf_so_loc");

        String trainFile = config.getOption("train");
        String modelFile = config.getOption("model");
        String templateFile = config.getOption("template");

        float c = Float.valueOf(config.getOption("c", "1"));
        int f = Integer.valueOf(config.getOption("f", "1"));
    }
}

