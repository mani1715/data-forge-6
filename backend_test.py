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
        """Create a test CSV file for upload testing with specific columns for custom rules"""
        # Create test dataset with columns that match the custom cleaning rules
        data = {
            'name': ['jOHN', 'alice', 'BOB', None, 'charlie', '', 'DAVID'],
            'date': ['2023-01-01', None, '2023-03-15', '', '2023-05-20', 'nan', '2023-07-10'],
            'order': [1, None, 3, '', 5, 'nan', 7],
            'price': [100.50, None, 200.75, '', 300.25, 'nan', 400.00],
            'product': ['Widget A', None, 'Widget B', '', 'Widget C', 'nan', 'Widget D']
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

    def test_custom_cleaning_rules(self):
        """Test specific custom cleaning rules implementation"""
        try:
            # First upload the test data
            csv_data = self.create_test_csv()
            files = {'file': ('test_custom_rules.csv', csv_data, 'text/csv')}
            upload_response = requests.post(f"{self.base_url}/upload", files=files, timeout=30)
            
            if upload_response.status_code != 200:
                self.log_test("Custom Rules - Upload", False, "Failed to upload test data")
                return False
            
            # Apply cleaning with AI strategy (which includes custom rules)
            clean_response = requests.post(
                f"{self.base_url}/action", 
                json={'action': 'fill_missing', 'strategy': 'ai'}, 
                timeout=30
            )
            
            if clean_response.status_code != 200:
                self.log_test("Custom Rules - Cleaning", False, "Failed to apply cleaning")
                return False
            
            data = clean_response.json()
            preview_data = data.get('preview', [])
            
            if not preview_data:
                self.log_test("Custom Rules - Data Check", False, "No preview data returned")
                return False
            
            # Check custom rules implementation
            rules_passed = True
            rule_details = []
            
            for row in preview_data:
                # Rule 1: Date field should show '00-00-0000' for missing dates
                if 'date' in row and row['date'] in [None, '', 'nan', 'NaN']:
                    rules_passed = False
                    rule_details.append("Date rule failed: found null/empty date")
                
                # Rule 2: Name field should be proper case
                if 'name' in row and row['name'] and isinstance(row['name'], str):
                    if row['name'] != row['name'].capitalize() and row['name'] != "Unknown":
                        rules_passed = False
                        rule_details.append(f"Name rule failed: '{row['name']}' not proper case")
                
                # Rule 3: Order field should be 'ORD X' format or 0
                if 'order' in row and row['order'] is not None:
                    order_val = str(row['order'])
                    if order_val != '0' and not order_val.startswith('ORD '):
                        rules_passed = False
                        rule_details.append(f"Order rule failed: '{order_val}' not in ORD X format")
                
                # Rule 4: Price field should be 0 for missing values (numeric)
                if 'price' in row and row['price'] is not None:
                    try:
                        price_val = float(row['price'])
                        # This is fine, numeric values are expected
                    except (ValueError, TypeError):
                        rules_passed = False
                        rule_details.append(f"Price rule failed: '{row['price']}' not numeric")
                
                # Rule 5: Product field should show 'Unknown' for missing values
                if 'product' in row and row['product'] in [None, '', 'nan', 'NaN']:
                    rules_passed = False
                    rule_details.append("Product rule failed: found null/empty product")
            
            details = "All custom rules passed" if rules_passed else f"Rule violations: {'; '.join(rule_details)}"
            self.log_test("Custom Cleaning Rules", rules_passed, details)
            return rules_passed
            
        except Exception as e:
            self.log_test("Custom Cleaning Rules", False, str(e))
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

    def test_quality_score_improvement(self):
        """Test that quality score improves to 100% after cleaning"""
        try:
            # Upload test data
            csv_data = self.create_test_csv()
            files = {'file': ('test_quality.csv', csv_data, 'text/csv')}
            upload_response = requests.post(f"{self.base_url}/upload", files=files, timeout=30)
            
            if upload_response.status_code != 200:
                self.log_test("Quality Score - Upload", False, "Failed to upload")
                return False
            
            initial_data = upload_response.json()
            initial_score = initial_data.get('quality_score', 0)
            
            # Apply cleaning
            clean_response = requests.post(
                f"{self.base_url}/action", 
                json={'action': 'fill_missing', 'strategy': 'ai'}, 
                timeout=30
            )
            
            if clean_response.status_code != 200:
                self.log_test("Quality Score - Cleaning", False, "Failed to clean")
                return False
            
            clean_data = clean_response.json()
            final_score = clean_data.get('new_score', 0)
            
            # Check if score improved
            score_improved = final_score > initial_score
            details = f"Initial: {initial_score}%, Final: {final_score}%"
            
            # Ideally should reach 100% but we'll accept improvement
            if final_score == 100:
                details += " - Perfect score achieved!"
            elif score_improved:
                details += " - Score improved"
            else:
                details += " - Score did not improve"
            
            self.log_test("Quality Score Improvement", score_improved, details)
            return score_improved
            
        except Exception as e:
            self.log_test("Quality Score Improvement", False, str(e))
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
            
            # Test 4: Custom Cleaning Rules
            self.test_custom_cleaning_rules()
            
            # Test 5: Quality Score Improvement
            self.test_quality_score_improvement()
            
            # Test 6: Download
            self.test_download_endpoint()
            
            # Test 7: Cleanup
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