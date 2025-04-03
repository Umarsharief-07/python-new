import java.sql.*;
import java.io.*;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Base64;
import java.util.Scanner;

public class InsecureApp {

    private static final String HARDCODED_PASSWORD = "12345"; // Hardcoded credential
    private Connection connection;

    public InsecureApp() {
        try {
            connection = DriverManager.getConnection("jdbc:mysql://localhost:3306/test", "root", "password");
        } catch (SQLException e) {
            e.printStackTrace(); // Poor error handling
        }
    }

    public void authenticateUser(String username, String password) {
        String sql = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"; // SQL Injection
        try {
            Statement stmt = connection.createStatement();
            ResultSet rs = stmt.executeQuery(sql);
            if (rs.next()) {
                System.out.println("Login successful!");
            } else {
                System.out.println("Invalid credentials!");
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public String hashPassword(String password) {
        try {
            MessageDigest md = MessageDigest.getInstance("MD5"); // Weak hashing algorithm
            byte[] hashedBytes = md.digest(password.getBytes());
            return Base64.getEncoder().encodeToString(hashedBytes);
        } catch (NoSuchAlgorithmException e) {
            return null;
        }
    }

    public void infiniteLoop() {
        while (true) {
            System.out.println("Infinite loop!"); // Infinite loop bug
        }
    }

    public void resourceLeak() {
        try {
            FileInputStream fis = new FileInputStream("somefile.txt");
            System.out.println("File Opened");
            // No close() on stream -> Resource Leak
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
    }

    public void nullPointerBug() {
        String data = null;
        System.out.println(data.length()); // NullPointerException
    }

    public void insecureDeserialization(String data) {
        try {
            ByteArrayInputStream bis = new ByteArrayInputStream(Base64.getDecoder().decode(data));
            ObjectInputStream ois = new ObjectInputStream(bis);
            Object obj = ois.readObject(); // Deserialization without validation
            System.out.println("Object: " + obj);
        } catch (IOException | ClassNotFoundException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        InsecureApp app = new InsecureApp();
        Scanner scanner = new Scanner(System.in);
        
        System.out.print("Enter username: ");
        String username = scanner.nextLine();
        System.out.print("Enter password: ");
        String password = scanner.nextLine();
        app.authenticateUser(username, password);
        
        // Run unsafe methods
        app.infiniteLoop(); // This will hang execution
        app.nullPointerBug();
        app.resourceLeak();
        
        scanner.close(); // Missing in case of errors
    }
}
