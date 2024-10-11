public class Redactor {
    public static String redact(String content, String[] redactWords) {
        String paddedContent = content + " ";
        StringBuilder redactedContent = new StringBuilder();
        StringBuilder currentWord = new StringBuilder();

        for (int i = 0; i < paddedContent.length(); i++) {
            char currentChar = paddedContent.charAt(i);

            if (!Character.isLetterOrDigit(currentChar) && currentChar != '!') {
                if (currentWord.length() > 0) {
                    String wordString = currentWord.toString();
                    boolean isRedactable = false;

                    for (String redactWord : redactWords) {
                        if (wordString.equalsIgnoreCase(redactWord)) {
                            isRedactable = true;
                            break;
                        }
                    }

                    if (isRedactable) {
                        for (int j = 0; j < wordString.length(); j++) {
                            redactedContent.append('*');
                        }
                    } else {
                        redactedContent.append(wordString);
                    }

                    currentWord = new StringBuilder();
                }

                redactedContent.append(currentChar);
            } else {
                currentWord.append(currentChar);
            }
        }

        return redactedContent.toString().trim();
    }

    public static void main(String[] args) {
        String content = "The quick brown p.ass pass123, but not p1ss or pass.";
        String[] redactWords = {"pass"};
        System.out.println(redact(content, redactWords));
    }
}