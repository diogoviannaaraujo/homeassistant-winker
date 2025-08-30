#!/usr/bin/env python3
"""Test script for Winker API functionality."""
import asyncio
import os
from winker_api import WinkerAPI


async def test_authentication():
    """Test the authentication functionality."""
    print("=" * 50)
    print("Testing Authentication")
    print("=" * 50)
    
    # You can set these as environment variables or modify them here
    email = os.getenv("WINKER_EMAIL", "your_email@example.com")
    password = os.getenv("WINKER_PASSWORD", "examplepassword")
    
    if email == "your_email@example.com":
        print("⚠️  Please set WINKER_EMAIL and WINKER_PASSWORD environment variables")
        print("   or modify the email/password in this script")
        return None
    
    api = WinkerAPI()
    
    try:
        token = await api.authenticate(email, password)
        if token:
            print("✅ Authentication successful!")
            print(f"Token (first 50 chars): {token[:50]}...")
            return api
        else:
            print("❌ Authentication failed - invalid credentials")
            return None
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return None


async def test_fetch_doors(api):
    """Test fetching doors from the API."""
    print("\n" + "=" * 50)
    print("Testing Fetch Doors")
    print("=" * 50)
    
    try:
        doors = await api.fetch_doors()
        
        if doors:
            print(f"✅ Successfully fetched {len(doors)} doors:")
            for door in doors:
                print(f"   • ID: {door.get('id_device', 'N/A')}, Name: {door.get('name', 'N/A')}")
        else:
            print("⚠️  No doors found or API call failed")
            
    except Exception as e:
        print(f"❌ Error fetching doors: {e}")


async def test_fetch_cameras(api):
    """Test fetching cameras from the API."""
    print("\n" + "=" * 50)
    print("Testing Fetch Cameras")
    print("=" * 50)
    
    try:
        cameras = await api.fetch_cameras()
        
        if cameras:
            print(f"✅ Successfully fetched {len(cameras)} cameras:")
            for camera in cameras:
                print(f"   • ID: {camera.get('id_camera', 'N/A')}, Name: {camera.get('name', 'N/A')}")
            return cameras
        else:
            print("⚠️  No cameras found or API call failed")
            return []
            
    except Exception as e:
        print(f"❌ Error fetching cameras: {e}")
        return []


async def test_fetch_camera_details(api, cameras):
    """Test fetching individual camera details."""
    if not cameras:
        print("\n⚠️  Skipping camera details test - no cameras available")
        return
        
    print("\n" + "=" * 50)
    print("Testing Fetch Camera Details")
    print("=" * 50)
    
    # Test with the first camera
    camera_id = cameras[0].get('id_camera')
    if not camera_id:
        print("⚠️  No camera ID available for testing")
        return
        
    try:
        camera_details = await api.fetch_camera(camera_id)
        
        if camera_details:
            print(f"✅ Successfully fetched details for camera {camera_id}:")
            print(f"   • Name: {camera_details.get('name', 'N/A')}")
            print(f"   • Status: {camera_details.get('status', 'N/A')}")
        else:
            print(f"⚠️  No details found for camera {camera_id}")
            
    except Exception as e:
        print(f"❌ Error fetching camera details: {e}")


async def test_with_hardcoded_token():
    """Test API functionality using the hardcoded token (fallback)."""
    print("\n" + "=" * 50)
    print("Testing with Hardcoded Token (Fallback)")
    print("=" * 50)
    
    api = WinkerAPI()  # No token provided, will use hardcoded one
    
    try:
        doors = await api.fetch_doors()
        print(f"✅ Hardcoded token test - fetched {len(doors) if doors else 0} doors")
    except Exception as e:
        print(f"❌ Hardcoded token test failed: {e}")


async def main():
    """Run all tests."""
    print("🚀 Starting Winker API Tests")
    
    # Test authentication
    api = await test_authentication()
    
    if api:
        # Test API functionality with authenticated instance
        await test_fetch_doors(api)
        cameras = await test_fetch_cameras(api)
        await test_fetch_camera_details(api, cameras)
    else:
        print("\n⚠️  Skipping authenticated tests due to authentication failure")
    
    # Test fallback to hardcoded token
    await test_with_hardcoded_token()
    
    print("\n" + "=" * 50)
    print("🏁 Tests completed!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
