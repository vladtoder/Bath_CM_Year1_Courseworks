public class SortedLinkedList implements SortedList {
    private Node head;
    private Node tail;

        @Override
        public int size() {
            int counter = 0;
            Node currentNode = head;

            while (currentNode != null) {
                counter++;
                currentNode = currentNode.getNext();
            }
            return counter;
        }

        @Override
        public void add(String string) {
            Node newNode = new Node(string);
            add(newNode);
        }

        @Override
        public void add(Node node) {
            if (isPresent(node.getString())) {
                return;
            }

            Node tempo = node;
            while (tempo != null) {
                Node nextNode = tempo.getNext();
                tempo.setNext(null);

                if (head == null) {
                    head = tempo;
                    tail = tempo;
                }
                else {
                    Node currentNode = head;
                    boolean inserted = false;
                    while (currentNode != null) {
                        if (tempo.getString().compareToIgnoreCase(currentNode.getString()) < 0) {
                            tempo.setNext(currentNode);
                            tempo.setPrev(currentNode.getPrev());

                            if (currentNode.getPrev() != null) {
                                currentNode.getPrev().setNext(tempo);
                            } else {
                                head = tempo;
                            }
                            currentNode.setPrev(tempo);
                            inserted = true;
                            break;
                        }
                        currentNode = currentNode.getNext();
                    }

                    if (!inserted) {
                        tail.setNext(tempo);
                        tempo.setPrev(tail);
                        tail = tempo;
                    }
                }

                tempo = nextNode;
            }
        }


        @Override
        public Node getFirst() {
            return head;
        }

        @Override
        public Node getLast() {
            return tail;
        }

        @Override
        public Node get(int index) {
            Node currentNode = head;
            int currentIndex = 0;

            while (currentNode != null && currentIndex < index) {
                currentNode = currentNode.getNext();
                currentIndex++;
            }
            return currentNode;
        }

        @Override
        public boolean isPresent(String string) {
            Node currentNode = head;

            while (currentNode != null) {
                if (currentNode.getString().equalsIgnoreCase(string)) {
                    return true;
                }
                currentNode = currentNode.getNext();
            }
            return false;
        }

        @Override
        public boolean removeFirst() {
            if (head == null) {
                return false;
            }

            Node toRemove = head;

            if (head.getNext() != null) {
                head = head.getNext();
                head.setPrev(null);
            }
            else {
                head = tail;
                tail = null;
            }
            toRemove.setNext(null);
            return true;
        }

        @Override
        public boolean removeLast() {
            if (tail == null) {
                return false;
            }

            Node toRemove = tail;

            if (tail.getPrev() != null) {
                tail = tail.getPrev();
                tail.setNext(null);
            }
            else {
                head = tail;
                tail = null;
            }
            toRemove.setPrev(null);
            return true;
        }

        @Override
        public boolean remove(int index) {
            if (index < 0 || index >= size()) {
                return false;
            }
            if (index == 0) {
                return removeFirst();
            }

            Node currentNode = get(index);

            if (currentNode != null) {
                if (currentNode.getNext() != null) {
                    currentNode.getNext().setPrev(currentNode.getPrev());
                }
                else {
                    tail = currentNode.getPrev();
                }
                if (currentNode.getPrev() != null) {
                    currentNode.getPrev().setNext(currentNode.getNext());
                }
                else {
                    head = currentNode.getNext();
                }
                currentNode.setNext(null);
                currentNode.setPrev(null);
                return true;
            }
            return false;
        }

        @Override
        public boolean remove(String string) {
            Node currentNode = head;

            while (currentNode != null) {
                if (currentNode.getString().equalsIgnoreCase(string)) {
                    if (currentNode.getPrev() != null) {
                        currentNode.getPrev().setNext(currentNode.getNext());
                    }
                    else {
                        head = currentNode.getNext();
                    }
                    if (currentNode.getNext() != null) {
                        currentNode.getNext().setPrev(currentNode.getPrev());
                    }
                    else {
                        tail = currentNode.getPrev();
                    }
                    currentNode.setNext(null);
                    currentNode.setPrev(null);
                    return true;
                }
                currentNode = currentNode.getNext();
            }
            return false;
        }

        @Override
        public void orderAscending() {
            boolean wasSwapped = true;

            while (wasSwapped) {
                wasSwapped = false;
                Node currentNode = head;

                while (currentNode != null && currentNode.getNext() != null) {
                    Node nextNode = currentNode.getNext();

                    if (currentNode.getString().compareToIgnoreCase(nextNode.getString()) > 0) {
                        String tempo = currentNode.getString();
                        currentNode.setString(nextNode.getString());
                        nextNode.setString(tempo);
                        wasSwapped = true;
                    }
                    currentNode = currentNode.getNext();
                }
            }
        }



        @Override
        public void orderDescending() {
            boolean wasSwapped = true;

            while (wasSwapped) {
                wasSwapped = false;
                Node currentNode = tail;

                while (currentNode != null && currentNode.getPrev() != null) {
                    Node prevNode = currentNode.getPrev();

                    if (currentNode.getString().compareToIgnoreCase(prevNode.getString()) > 0) {
                        String tempo = currentNode.getString();
                        currentNode.setString(prevNode.getString());
                        prevNode.setString(tempo);
                        wasSwapped = true;
                    }
                    currentNode = currentNode.getPrev();
                }
            }
        }


        @Override
        public void print() {
            Node currentNode = head;
            while (currentNode != null) {
                System.out.println(currentNode.getString());
                currentNode = currentNode.getNext();
            }
        }
}