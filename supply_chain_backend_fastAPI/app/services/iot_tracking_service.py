# app/services/iot_tracking_service.py
import asyncio
import json
import logging
import random
import time
from typing import Dict, Any, List, Optional, Callable
from azure.iot.device.aio import IoTHubDeviceClient, IoTHubServiceClient
from azure.iot.device import Message
import os

class IoTTrackingService:
    """Service for handling IoT device tracking data"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(IoTTrackingService, cls).__new__(cls)
            cls._instance.service_client = None
            cls._instance.device_clients = {}
            cls._instance.is_simulating = False
            cls._instance.simulation_task = None
            cls._instance.callbacks = []
        return cls._instance
    
    async def initialize_service_client(self):
        """Initialize the IoT Hub service client"""
        try:
            connection_string = os.environ.get("AZURE_IOT_HUB_CONNECTION_STRING", "")
            if not connection_string:
                logging.error("Azure IoT Hub connection string not found")
                return False
                
            self.service_client = IoTHubServiceClient.from_connection_string(connection_string)
            logging.info("Azure IoT Hub service client initialized successfully")
            return True
        except Exception as e:
            logging.error(f"Error initializing Azure IoT Hub service client: {e}")
            return False
    
    async def register_device(self, device_id: str) -> Dict[str, Any]:
        """Register a new device with IoT Hub"""
        try:
            if not self.service_client:
                await self.initialize_service_client()
                
            # In a real implementation, this would register the device with IoT Hub
            # and return the device connection string
            
            # For this example, we'll simulate a successful registration
            device_info = {
                "device_id": device_id,
                "status": "registered",
                "connection_status": "connected"
            }
            
            return device_info
        except Exception as e:
            logging.error(f"Error registering device {device_id}: {e}")
            return {"device_id": device_id, "status": "error", "message": str(e)}
    
    async def get_device_status(self, device_id: str) -> Dict[str, Any]:
        """Get the status of a device"""
        try:
            if not self.service_client:
                await self.initialize_service_client()
                
            # In a real implementation, this would query IoT Hub for device status
            
            # For this example, we'll simulate a device status
            device_status = {
                "device_id": device_id,
                "connection_status": "connected" if device_id in self.device_clients else "disconnected",
                "last_activity": time.time(),
                "battery_level": random.randint(20, 100),
                "firmware_version": "1.2.3"
            }
            
            return device_status
        except Exception as e:
            logging.error(f"Error getting status for device {device_id}: {e}")
            return {"device_id": device_id, "status": "error", "message": str(e)}
    
    async def send_command_to_device(self, device_id: str, command_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send a command to a device"""
        try:
            if not self.service_client:
                await self.initialize_service_client()
                
            # In a real implementation, this would send a command to the device via IoT Hub
            
            # For this example, we'll simulate a successful command
            response = {
                "device_id": device_id,
                "command": command_name,
                "status": "success",
                "response_payload": {"acknowledged": True, "timestamp": time.time()}
            }
            
            return response
        except Exception as e:
            logging.error(f"Error sending command to device {device_id}: {e}")
            return {"device_id": device_id, "status": "error", "message": str(e)}
    
    async def start_tracking_simulation(self, num_vehicles: int = 5, interval: int = 10):
        """Start simulating vehicle tracking data"""
        if self.is_simulating:
            return {"status": "already_running"}
        
        self.is_simulating = True
        self.simulation_task = asyncio.create_task(self._run_simulation(num_vehicles, interval))
        
        return {"status": "started", "num_vehicles": num_vehicles, "interval": interval}
    
    async def stop_tracking_simulation(self):
        """Stop simulating vehicle tracking data"""
        if not self.is_simulating:
            return {"status": "not_running"}
        
        self.is_simulating = False
        if self.simulation_task:
            self.simulation_task.cancel()
            self.simulation_task = None
        
        return {"status": "stopped"}
    
    async def _run_simulation(self, num_vehicles: int, interval: int):
        """Run the tracking data simulation"""
        try:
            # Generate vehicle IDs
            vehicle_ids = [f"vehicle-{i+1}" for i in range(num_vehicles)]
            
            # Initial positions centered around a base location
            base_lat, base_lng = 40.7128, -74.0060  # Example: New York City
            positions = {}
            routes = {}
            
            # Generate random routes for each vehicle
            for vehicle_id in vehicle_ids:
                # Starting position with some random variation
                lat = base_lat + random.uniform(-0.05, 0.05)
                lng = base_lng + random.uniform(-0.05, 0.05)
                positions[vehicle_id] = {"lat": lat, "lng": lng}
                
                # Generate a random route with 5-10 waypoints
                num_waypoints = random.randint(5, 10)
                waypoints = []
                for _ in range(num_waypoints):
                    # Each waypoint is within reasonable distance from the previous one
                    waypoint_lat = lat + random.uniform(-0.02, 0.02)
                    waypoint_lng = lng + random.uniform(-0.02, 0.02)
                    waypoints.append({"lat": waypoint_lat, "lng": waypoint_lng})
                    lat, lng = waypoint_lat, waypoint_lng
                
                routes[vehicle_id] = waypoints
            
            # Simulate movement along routes
            route_positions = {vehicle_id: 0 for vehicle_id in vehicle_ids}
            
            while self.is_simulating:
                for vehicle_id in vehicle_ids:
                    # Get current route and position
                    route = routes[vehicle_id]
                    route_pos = route_positions[vehicle_id]
                    
                    # If we've reached the end of the route, start over
                    if route_pos >= len(route):
                        route_positions[vehicle_id] = 0
                        route_pos = 0
                    
                    # Get current waypoint
                    waypoint = route[route_pos]
                    
                    # Move slightly towards the waypoint
                    current_pos = positions[vehicle_id]
                    move_factor = random.uniform(0.1, 0.3)  # Random movement factor
                    
                    new_lat = current_pos["lat"] + (waypoint["lat"] - current_pos["lat"]) * move_factor
                    new_lng = current_pos["lng"] + (waypoint["lng"] - current_pos["lng"]) * move_factor
                    
                    # Check if we're close enough to the waypoint to move to the next one
                    if (abs(new_lat - waypoint["lat"]) < 0.001 and 
                        abs(new_lng - waypoint["lng"]) < 0.001):
                        route_positions[vehicle_id] = route_pos + 1
                    
                    # Update position
                    positions[vehicle_id] = {"lat": new_lat, "lng": new_lng}
                    
                    # Generate tracking data
                    tracking_data = {
                        "device_id": vehicle_id,
                        "timestamp": time.time(),
                        "position": {
                            "lat": new_lat,
                            "lng": new_lng
                        },
                        "speed": random.uniform(20, 65),  # Speed in km/h
                        "heading": random.uniform(0, 359),  # Heading in degrees
                        "status": random.choice(["in_transit", "loading", "unloading", "idle"]),
                        "cargo_temp": random.uniform(2.0, 8.0) if vehicle_id.endswith(("1", "3", "5")) else None,  # Temperature for refrigerated vehicles
                        "fuel_level": random.uniform(20, 100),  # Fuel level percentage
                        "battery_level": random.uniform(50, 100),  # Battery level percentage
                        "signal_strength": random.randint(1, 5)  # Signal strength 1-5
                    }
                    
                    # Notify callbacks with the tracking data
                    for callback in self.callbacks:
                        try:
                            callback(tracking_data)
                        except Exception as e:
                            logging.error(f"Error in tracking callback: {e}")
                    
                    # In a real implementation, this would send data to IoT Hub
                    # await self._send_tracking_data_to_iot_hub(vehicle_id, tracking_data)
                
                # Wait for the next interval
                await asyncio.sleep(interval)
                
        except asyncio.CancelledError:
            logging.info("Tracking simulation cancelled")
        except Exception as e:
            logging.error(f"Error in tracking simulation: {e}")
            self.is_simulating = False
    
    async def _send_tracking_data_to_iot_hub(self, device_id: str, data: Dict[str, Any]):
        """Send tracking data to IoT Hub"""
        try:
            # Get or create device client
            device_client = self.device_clients.get(device_id)
            if not device_client:
                # In a real implementation, we would get the device connection string from a secure store
                connection_string = os.environ.get("AZURE_IOT_HUB_DEVICE_CONNECTION_STRING", "")
                if not connection_string:
                    logging.error(f"Device connection string not found for {device_id}")
                    return False
                
                # Create device client
                device_client = IoTHubDeviceClient.from_connection_string(connection_string)
                await device_client.connect()
                self.device_clients[device_id] = device_client
            
            # Create message
            message = Message(json.dumps(data))
            message.content_type = "application/json"
            message.content_encoding = "utf-8"
            
            # Send message
            await device_client.send_message(message)
            return True
        except Exception as e:
            logging.error(f"Error sending tracking data to IoT Hub for device {device_id}: {e}")
            return False
    
    def register_tracking_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """Register a callback function to receive tracking data"""
        if callback not in self.callbacks:
            self.callbacks.append(callback)
    
    def unregister_tracking_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """Unregister a tracking data callback function"""
        if callback in self.callbacks:
            self.callbacks.remove(callback)