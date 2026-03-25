#!/usr/bin/env python3
"""
DataForge Backend API Testing Suite
Tests all backend endpoints for functionality and integration
"""

import requests
import sys
import os
import io
import pandas as pd
from datetime import datetime

class DataForgeAPITester:
    def __init__(self, base_url="https://dataforge-preview.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}")
        else:
            print(f"❌ {name} - {details}")
        
        self.test_results.append({
            "test": name,
            "success": success,
            "details": details
        })

    def test_health_endpoint(self):
        """Test the health endpoint"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            if success:
                data = response.json()
                details += f", Response: {data}"
            self.log_test("Health Endpoint", success, details)
            return success
        except Exception as e:
            self.log_test("Health Endpoint", False, str(e))
            return False

    def create_test_csv(self):
        """Create a test CSV file for upload testing"""
        # Create a simple test dataset with some missing values and duplicates
        data = {
            'name': ['Alice', 'Bob', 'Charlie', 'Alice', 'David', None, 'Eve'],
            'age': [25, 30, None, 25, 35, 28, 22],
            'salary': [50000, 60000, 55000, 50000, None, 65000, 45000],
            'department': ['IT', 'HR', 'IT', 'IT', 'Finance', 'HR', None]
        }
        df = pd.DataFrame(data)
        
        # Save to BytesIO for upload
        csv_buffer = io.BytesIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        return csv_buffer

    def test_file_upload(self):
        """Test file upload functionality"""
        try:
            # Create test CSV
            csv_data = self.create_test_csv()
            
            files = {'file': ('test_data.csv', csv_data, 'text/csv')}
            response = requests.post(f"{self.base_url}/upload", files=files, timeout=30)
            
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success:
                data = response.json()
                required_fields = ['message', 'filename', 'quality_score', 'summary', 'preview']
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    success = False
                    details += f", Missing fields: {missing_fields}"
                else:
                    details += f", Score: {data.get('quality_score', 'N/A')}, Rows: {data.get('summary', {}).get('rows', 'N/A')}"
            else:
                try:
                    error_data = response.json()
                    details += f", Error: {error_data.get('error', 'Unknown error')}"
                except:
                    details += f", Response: {response.text[:100]}"
            
            self.log_test("File Upload", success, details)
            return success, response.json() if success else None
            
        except Exception as e:
            self.log_test("File Upload", False, str(e))
            return False, None

    def test_data_cleaning_actions(self):
        """Test data cleaning actions"""
        actions = [
            {'action': 'remove_duplicates'},
            {'action': 'fill_missing', 'strategy': 'ai'},
            {'action': 'remove_outliers'},
            {'action': 'clean_text'}
        ]
        
        all_passed = True
        for action_data in actions:
            try:
                response = requests.post(
                    f"{self.base_url}/action", 
                    json=action_data, 
                    timeout=30
                )
                
                success = response.status_code == 200
                action_name = action_data['action']
                details = f"Status: {response.status_code}"
                
                if success:
                    data = response.json()
                    required_fields = ['message', 'new_score', 'preview']
                    missing_fields = [field for field in required_fields if field not in data]
                    
                    if missing_fields:
                        success = False
                        details += f", Missing fields: {missing_fields}"
                    else:
                        details += f", New Score: {data.get('new_score', 'N/A')}"
                else:
                    try:
                        error_data = response.json()
                        details += f", Error: {error_data.get('error', 'Unknown error')}"
                    except:
                        details += f", Response: {response.text[:100]}"
                
                self.log_test(f"Clean Action: {action_name}", success, details)
                if not success:
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Clean Action: {action_name}", False, str(e))
                all_passed = False
        
        return all_passed

    def test_download_endpoint(self):
        """Test file download functionality"""
        try:
            response = requests.get(f"{self.base_url}/download", timeout=30)
            
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success:
                # Check if response is CSV
                content_type = response.headers.get('content-type', '')
                if 'csv' in content_type.lower() or 'text' in content_type.lower():
                    details += f", Content-Type: {content_type}, Size: {len(response.content)} bytes"
                else:
                    success = False
                    details += f", Unexpected Content-Type: {content_type}"
            else:
                try:
                    error_data = response.json()
                    details += f", Error: {error_data.get('error', 'Unknown error')}"
                except:
                    details += f", Response: {response.text[:100]}"
            
            self.log_test("Download Endpoint", success, details)
            return success
            
        except Exception as e:
            self.log_test("Download Endpoint", False, str(e))
            return False

    def test_cleanup_endpoint(self):
        """Test cleanup functionality"""
        try:
            response = requests.post(f"{self.base_url}/cleanup", timeout=10)
            
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success:
                data = response.json()
                details += f", Message: {data.get('message', 'N/A')}"
            else:
                try:
                    error_data = response.json()
                    details += f", Error: {error_data.get('error', 'Unknown error')}"
                except:
                    details += f", Response: {response.text[:100]}"
            
            self.log_test("Cleanup Endpoint", success, details)
            return success
            
        except Exception as e:
            self.log_test("Cleanup Endpoint", False, str(e))
            return False

    def run_full_test_suite(self):
        """Run complete backend test suite"""
        print("🚀 Starting DataForge Backend API Tests")
        print(f"📍 Testing against: {self.base_url}")
        print("=" * 60)
        
        # Test 1: Health Check
        health_ok = self.test_health_endpoint()
        
        if not health_ok:
            print("\n❌ Health check failed - stopping tests")
            return False
        
        # Test 2: File Upload
        upload_ok, upload_data = self.test_file_upload()
        
        if not upload_ok:
            print("\n❌ File upload failed - skipping dependent tests")
        else:
            # Test 3: Data Cleaning Actions (only if upload worked)
            self.test_data_cleaning_actions()
            
            # Test 4: Download
            self.test_download_endpoint()
            
            # Test 5: Cleanup
            self.test_cleanup_endpoint()
        
        # Print Summary
        print("\n" + "=" * 60)
        print(f"📊 Test Results: {self.tests_passed}/{self.tests_run} passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed!")
            return True
        else:
            print("⚠️  Some tests failed - check details above")
            return False

def main():
    """Main test execution"""
    tester = DataForgeAPITester()
    success = tester.run_full_test_suite()
    
    # Return appropriate exit code
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())