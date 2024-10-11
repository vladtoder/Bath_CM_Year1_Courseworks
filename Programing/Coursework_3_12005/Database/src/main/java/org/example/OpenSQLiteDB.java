package org.example;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class OpenSQLiteDB {
    public static void main(String[] args) {
        // Corrected path to your database file
        // Note: Make sure to escape backslashes in the file path or use forward slashes.
        String url = "jdbc:sqlite:D:\\database.db";

        try (Connection conn = DriverManager.getConnection(url)) {
            if (conn != null) {
                System.out.println("Connected to the database.");
                // You can now create statements and execute queries.
            }
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }
}
