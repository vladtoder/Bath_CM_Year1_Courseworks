import java.util.Collections;

public class Main {
    public static void main(String[] args) {
        String[] filenames = {"file1.txt", "file2.txt"};

        for (String filename : filenames) {
            Thread thread = new Thread(new PopThread(Collections.singletonList(filename)));
            thread.start();
        }
    }
}
