package org.example.app;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class AppIntegrationTest {
    @Test
    void testAppIntegration() {
        // This is a sample integration test
        App app = new App();
        assertNotNull(app.getGreeting());
    }
}