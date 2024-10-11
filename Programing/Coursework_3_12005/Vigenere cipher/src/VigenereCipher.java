import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class VigenereCipher implements Cipher {
    private String key;

    public VigenereCipher() {
    }

    @Override
    public String encrypt(String message_filename, String key_filename) {
        this.key = readFile(key_filename).toUpperCase();
        if (!isKeyValid(this.key)) {
            return "error. invalid key";
        }
        String message = readFile(message_filename).toUpperCase();
        return process(message, true);
    }

    @Override
    public String decrypt(String message_filename, String key_filename) {
        this.key = readFile(key_filename).toUpperCase();
        if (!isKeyValid(this.key)) {
            return "error. invalid key";
        }
        String encryptedMessage = readFile(message_filename).toUpperCase();
        return process(encryptedMessage, false);
    }

    private boolean isKeyValid(String key) {
        if (key == null || key.isEmpty()) return false;
        for (char c : key.toCharArray()) {
            if (!Character.isLetter(c)) return false;
        }
        return true;
    }

    private String process(String input, boolean encrypt) {
        if (this.key == null) {
            return "Operation cannot proceed due to an invalid key.";
        }

        StringBuilder output = new StringBuilder();
        input = input.toUpperCase();
        for (int i = 0, j = 0; i < input.length(); i++) {
            char letter = input.charAt(i);
            if (letter < 'A' || letter > 'Z') {
                output.append(letter);
                j++;
            } else {
                int keyIndex = key.charAt(j % key.length()) - 'A';
                int letterIndex = letter - 'A';
                if (encrypt) {
                    output.append((char) (((letterIndex + keyIndex) % 26) + 'A'));
                } else {
                    output.append((char) (((letterIndex - keyIndex + 26) % 26) + 'A'));
                }
                j++;
            }
        }
        return output.toString();
    }

    private String readFile(String filename) {
        StringBuilder content = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            String line;
            while ((line = reader.readLine()) != null) {
                content.append(line.toUpperCase());
                content.append("\n");
            }
            if (content.length() > 0) {
                content.setLength(content.length() - 1);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return content.toString();
    }
}

