import java.util.HashMap;
import java.util.Map;
import java.util.logging.Logger;

/** 
 * This implements a simple config parser.
 */


public class ConfigParser {
  private Map<String, String> options;
  private static final Logger logger = Logger.getLogger(ConfigParser.class.getSimpleName());
  
  public ConfigParser(final String[] args) {
    options = new HashMap<String, String>();
    for (int i = 0; i < args.length; ++i) {
      // Key contains word-chars only, and Value cannot contain space or =.
      if (args[i].matches("--\\w+=[^\\s=]+")) {
        String[] fds = args[i].trim().split("=");
        if (fds.length != 2) {
          logger.severe("Wrong option line " + args[i]);
          System.exit(1);
        }
        fds[0] = fds[0].replace("--", "");
        options.put(fds[0].trim(), fds[1].trim());
      } else {
        logger.severe("Wrong option line " + args[i]);
        System.exit(1);
      }
    }    
  }
  
  public ConfigParser() {
    options = new HashMap<String, String>();
  }
 
  public void addOption(final String key, String val) {
    options.put(key, val);
  }
  
  public boolean hasOption(final String key) {
    return options.containsKey(key);
  }
  
  public String getOption(final String key) {
    return options.get(key);
  }
  
  public String getOption(final String key, final String defaultVal) {
    String res = options.get(key);
    if (res == null) {
      res = defaultVal;
    } 
    return res;
  }
  
  public void checkRequiredArgs(final String[] args) {
    for (String arg : args) {
      if (hasOption(arg) != true) {
        logger.severe("Does not have required arg " + arg);
        System.exit(1);
      }
    }
  }
  
  public void printOptions() {
    logger.info("======= Set of options are ================");
    for (String key : options.keySet()) {
      logger.info("key=" + key + "; val=" + options.get(key));
    }
  }
}

