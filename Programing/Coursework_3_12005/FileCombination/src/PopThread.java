import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class PopThread implements Runnable {
    private List<String> filenames;

    public PopThread(List<String> filenames) {
        this.filenames = new ArrayList<>(filenames);
    }

    @Override
    public void run() {
        filenames.forEach(filename -> {
            StringBuilder content = new StringBuilder();
            String order = null;

            try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
                String line;

                while ((line = reader.readLine()) != null) {
                    content.append(line).append(System.lineSeparator());
                    if (line.startsWith("#")) {
                        order = line.substring(line.indexOf("#") + 1, line.indexOf("/"));
                    }
                }
            } catch (IOException e) {
                e.printStackTrace();
            }

            if (order != null) {
                while (!isTurn(Integer.parseInt(order))) {
                    try {
                        Thread.sleep(100); // Wait before checking again
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        return;
                    }
                }
                writeToResultFile(content.toString());
            }
        });
    }

    private void writeToResultFile(String content) {
        synchronized (PopThread.class) {
            try (FileWriter writer = new FileWriter("result.txt", true)) {
                writer.write(content);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    private boolean isTurn(int order) {

        try (BufferedReader reader = new BufferedReader(new FileReader("result.txt"))) {
            String lastLine = "";
            String line;
            while ((line = reader.readLine()) != null) {
                lastLine = line;
            }
            if (!lastLine.isEmpty() && lastLine.startsWith("#")) {
                int lastOrder = Integer.parseInt(lastLine.substring(1, lastLine.indexOf("/")));
                return order == lastOrder + 1;
            }
        } catch (FileNotFoundException e) {
            return order == 1;
        } catch (IOException e) {
            e.printStackTrace();
        }
        return false;
    }
}
