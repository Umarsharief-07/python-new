import java.io.*;
import java.sql.*;
import java.util.Scanner;

public class VulnerableApp {
    
    // 🔥 Security Risk: Hardcoded credentials
    private static final String DB_USER = "admin";
    private static final String DB_PASS = "password123";

    // 🔥 Insecure Logging (Logging Sensitive Info)
    public static void log(String message) {
        System.out.println("[LOG]: " + message); // ❌ Logs sensitive info
    }

    // ❌ SQL Injection Vulnerability
    public static void sqlInjection(String username) {
        try (Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/test", DB_USER, DB_PASS);
             Statement stmt = conn.createStatement()) {

            String query = "SELECT * FROM users WHERE username = '" + username + "'";  // ❌ SQL Injection risk
            ResultSet rs = stmt.executeQuery(query);

            while (rs.next()) {
                System.out.println("User found: " + rs.getString("username"));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    // ❌ Command Injection
    public static void executeCommand(String command) throws IOException {
        Runtime.getRuntime().exec(command); // 🔥 Security Risk: Allows arbitrary command execution
    }

    // ❌ Unsafe Deserialization (RCE Risk)
    public static Object insecureDeserialization(byte[] data) throws IOException, ClassNotFoundException {
        ByteArrayInputStream bis = new ByteArrayInputStream(data);
        ObjectInputStream ois = new ObjectInputStream(bis);
        return ois.readObject(); // 🔥 Security Risk: Arbitrary code execution possible
    }

    // ❌ Division by Zero
    public static int divide(int a, int b) {
        return a / b; // ❌ Crashes when b == 0
    }

    // ❌ Null Pointer Dereference
    public static void nullPointerBug() {
        String text = null;
        System.out.println(text.length()); // ❌ NullPointerException
    }

    // ❌ Infinite Loop
    public static void infiniteLoop() {
        while (true) {  // ❌ DoS vulnerability
            System.out.println("Looping forever...");
        }
    }

    // ❌ Array Index Out of Bounds
    public static void arrayOutOfBounds() {
        int[] arr = {1, 2, 3};
        System.out.println(arr[5]); // ❌ IndexOutOfBoundsException
    }

    public static void main(String[] args) {
        log("Starting application...");

        // SQL Injection Demo
        Scanner scanner = new Scanner(System.in);
        System.out.println("Enter username:");
        String userInput = scanner.nextLine();
        sqlInjection(userInput);

        // Call unsafe functions
        try {
            executeCommand("rm -rf /"); // ❌ DANGEROUS
        } catch (IOException e) {
            e.printStackTrace();
        }

        try {
            System.out.println(divide(10, 0)); // ❌ Will crash
        } catch (Exception e) {
            log("Error: " + e.getMessage());
        }

        nullPointerBug();
        arrayOutOfBounds();
    }
}
