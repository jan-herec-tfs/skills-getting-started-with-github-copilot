"""Tests for GET /activities endpoint"""
import pytest


class TestGetActivities:
    """Test suite for retrieving activities"""
    
    def test_get_activities_returns_all_activities(self, client):
        """
        Arrange: Set up client with endpoint
        Act: Fetch all activities
        Assert: Verify response contains all activities with correct structure
        """
        # Arrange
        expected_activities = ["Chess Club", "Programming Class", "Gym Class"]
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert all(activity in data for activity in expected_activities)
    
    def test_get_activities_returns_activity_details(self, client):
        """
        Arrange: Set up client
        Act: Fetch activities
        Assert: Verify activity has required fields
        """
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity in data.values():
            for field in required_fields:
                assert field in activity, f"Missing field: {field}"
    
    def test_get_activities_participants_are_list(self, client):
        """
        Arrange: Set up client
        Act: Fetch activities
        Assert: Verify participants field is a list
        """
        # Arrange & Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity in data.values():
            assert isinstance(activity["participants"], list)
    
    def test_get_activities_contains_expected_participant_count(self, client):
        """
        Arrange: Set up client
        Act: Fetch activities
        Assert: Verify specific participant counts
        """
        # Arrange
        expected_counts = {
            "Chess Club": 2,
            "Programming Class": 2,
            "Gym Class": 2
        }
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, expected_count in expected_counts.items():
            assert len(data[activity_name]["participants"]) == expected_count
