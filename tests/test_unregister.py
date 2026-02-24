"""Tests for DELETE /activities/{activity_name}/unregister endpoint"""
import pytest


class TestUnregisterFromActivity:
    """Test suite for unregistering from activities"""
    
    def test_unregister_successful_removes_participant(self, client):
        """
        Arrange: Get current participant from activity
        Act: Send unregister request
        Assert: Verify participant is removed
        """
        # Arrange
        activity = "Chess Club"
        get_response = client.get("/activities")
        participants = get_response.json()[activity]["participants"]
        email_to_remove = participants[0]
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email_to_remove}
        )
        
        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        
        # Verify participant was actually removed
        verify_response = client.get("/activities")
        updated_participants = verify_response.json()[activity]["participants"]
        assert email_to_remove not in updated_participants
    
    def test_unregister_nonexistent_activity_fails(self, client):
        """
        Arrange: Prepare email and nonexistent activity
        Act: Send unregister request for invalid activity
        Assert: Verify request fails with 404 status
        """
        # Arrange
        email = "student@mergington.edu"
        nonexistent_activity = "Underwater Basket Weaving"
        
        # Act
        response = client.delete(
            f"/activities/{nonexistent_activity}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_unregister_not_registered_student_fails(self, client):
        """
        Arrange: Prepare email not in activity
        Act: Send unregister request for student not registered
        Assert: Verify request fails with 400 status
        """
        # Arrange
        email = "notregistered@mergington.edu"
        activity = "Chess Club"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"].lower()
    
    def test_unregister_preserves_other_participants(self, client):
        """
        Arrange: Get activity with multiple participants
        Act: Unregister one participant
        Assert: Verify other participants remain
        """
        # Arrange
        activity = "Gym Class"
        get_response = client.get("/activities")
        original_participants = get_response.json()[activity]["participants"].copy()
        
        email_to_remove = original_participants[0]
        other_participants = original_participants[1:]
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email_to_remove}
        )
        
        # Assert
        assert response.status_code == 200
        verify_response = client.get("/activities")
        remaining_participants = verify_response.json()[activity]["participants"]
        
        for email in other_participants:
            assert email in remaining_participants
    
    def test_unregister_and_resign_up(self, client):
        """
        Arrange: Get participant from activity
        Act: Unregister then sign up again
        Assert: Verify signup succeeds after unregister
        """
        # Arrange
        activity = "Programming Class"
        get_response = client.get("/activities")
        email = get_response.json()[activity]["participants"][0]
        
        # Act - unregister
        unregister_response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        # Assert unregister succeeded
        assert unregister_response.status_code == 200
        
        # Act - sign up again
        signup_response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert signup after unregister succeeded
        assert signup_response.status_code == 200
        verify_response = client.get("/activities")
        assert email in verify_response.json()[activity]["participants"]
