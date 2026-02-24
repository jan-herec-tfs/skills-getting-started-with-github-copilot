"""Tests for POST /activities/{activity_name}/signup endpoint"""
import pytest


class TestSignupForActivity:
    """Test suite for signing up for activities"""
    
    def test_signup_successful_adds_participant(self, client):
        """
        Arrange: Prepare email and activity name
        Act: Send signup request
        Assert: Verify participant is added and response is successful
        """
        # Arrange
        email = "newstudent@mergington.edu"
        activity = "Chess Club"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        
        # Verify participant was actually added
        verify_response = client.get("/activities")
        participants = verify_response.json()[activity]["participants"]
        assert email in participants
    
    def test_signup_duplicate_registration_fails(self, client):
        """
        Arrange: Prepare email already in activity
        Act: Attempt to sign up twice
        Assert: Verify second signup fails with 400 status
        """
        # Arrange
        email = "newstudent@mergington.edu"
        activity = "Chess Club"
        
        # Act - first signup
        response1 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert first signup succeeded
        assert response1.status_code == 200
        
        # Act - attempt duplicate signup
        response2 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert duplicate signup failed
        assert response2.status_code == 400
        assert "already registered" in response2.json()["detail"].lower()
    
    def test_signup_nonexistent_activity_fails(self, client):
        """
        Arrange: Prepare email and nonexistent activity
        Act: Send signup request for invalid activity
        Assert: Verify request fails with 404 status
        """
        # Arrange
        email = "student@mergington.edu"
        nonexistent_activity = "Underwater Basket Weaving"
        
        # Act
        response = client.post(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_signup_multiple_students_to_same_activity(self, client):
        """
        Arrange: Prepare multiple unique emails
        Act: Sign up multiple students
        Assert: Verify all are added successfully
        """
        # Arrange
        activity = "Programming Class"
        emails = ["alice@mergington.edu", "bob@mergington.edu", "charlie@mergington.edu"]
        
        # Act & Assert - sign up each student
        for email in emails:
            response = client.post(
                f"/activities/{activity}/signup",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Verify all students are in activity
        verify_response = client.get("/activities")
        participants = verify_response.json()[activity]["participants"]
        for email in emails:
            assert email in participants
    
    def test_signup_preserves_existing_participants(self, client):
        """
        Arrange: Prepare new email
        Act: Sign up new student
        Assert: Verify existing participants remain
        """
        # Arrange
        activity = "Gym Class"
        original_response = client.get("/activities")
        original_participants = original_response.json()[activity]["participants"].copy()
        
        new_email = "newestudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": new_email}
        )
        
        # Assert
        assert response.status_code == 200
        verify_response = client.get("/activities")
        updated_participants = verify_response.json()[activity]["participants"]
        
        for original_email in original_participants:
            assert original_email in updated_participants
