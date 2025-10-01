import pytest
import sys
import os

from app.app import create_app

class TestUnit:
    def test_app_creation(self):
        """Test that the app creates correctly"""
        app = create_app({
            'TESTING': True,
            'DATABASE': 'test.db',
            'SECRET_KEY': 'test-key'
        })
        assert app is not None
        assert app.config['TESTING'] == True

    def test_index_route(self, client):
        """Test the index route returns 200"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'SecureNote' in response.data

    def test_add_note_valid(self, client):
        """Test adding a valid note via POST"""
        response = client.post('/add', data={
            'title': 'Test Note',
            'content': 'Test Content'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'success' in response.data

    def test_add_note_empty_content(self, client):
        """Test adding a note with empty content"""
        response = client.post('/add', data={
            'title': 'Test Note',
            'content': ''
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'empty' in response.data