import requests
import json
import random
import datetime
from faker import Faker
import uuid

# Initialize Faker
fake = Faker()
base_url = "http://localhost:8000"  # Replace with your actual API base URL

# Helper function to generate unique IDs
def generate_id():
    return str(uuid.uuid4())

# ------------------- Data Section -------------------
def generate_product():
    categories = ["Electronics", "Clothing", "Furniture", "Food", "Books", "Sports"]
    # Using proper Faker methods instead of product_name which doesn't exist
    return {
        "product_id": generate_id(),
        "name": f"{fake.word().capitalize()} {random.choice(['Premium', 'Basic', 'Pro', 'Ultra', 'Lite'])} {random.choice(['Device', 'Item', 'Product', 'Tool', 'Kit'])}",
        "category": random.choice(categories),
        "price": round(random.uniform(10.0, 1000.0), 2),
        "cost": round(random.uniform(5.0, 800.0), 2),
        "sku": fake.bothify(text='SKU-????-########'),
        "created_at": fake.date_time_this_year().isoformat()
    }

def generate_inventory_item(product_id):
    warehouses = ["Main Warehouse", "East Coast DC", "West Coast DC", "Central Storage", "International Hub"]
    return {
        "inventory_id": generate_id(),
        "product_id": product_id,
        "quantity": random.randint(0, 1000),
        "location": random.choice(warehouses),
        "last_restocked": fake.date_time_this_month().isoformat(),
        "min_stock_level": random.randint(5, 50),
        "max_stock_level": random.randint(100, 2000)
    }

def generate_sales_data(product_id):
    return {
        "sales_id": generate_id(),
        "product_id": product_id,
        "quantity": random.randint(1, 100),
        "revenue": round(random.uniform(100.0, 10000.0), 2),
        "transaction_date": fake.date_time_this_year().isoformat(),
        "channel": random.choice(["Online", "In-store", "Partner", "Wholesale"]),
        "customer_region": fake.country()
    }

def generate_logistics_data(product_id, inventory_id):
    statuses = ["Shipped", "In Transit", "Delivered", "Processing", "On Hold"]
    return {
        "logistics_id": generate_id(),
        "product_id": product_id,
        "inventory_id": inventory_id,
        "quantity": random.randint(1, 50),
        "origin": fake.city(),
        "destination": fake.city(),
        "status": random.choice(statuses),
        "estimated_arrival": fake.future_date().isoformat(),
        "actual_arrival": fake.date_time_this_month().isoformat() if random.random() > 0.3 else None,
        "carrier": random.choice(["FedEx", "UPS", "DHL", "USPS", "Amazon Logistics"])
    }

def upload_sample_data():
    # Generate a batch of product data
    products = [generate_product() for _ in range(20)]
    product_ids = [p["product_id"] for p in products]
    
    # Generate inventory for each product
    inventory_items = []
    for product_id in product_ids:
        for _ in range(random.randint(1, 3)):
            inventory_items.append(generate_inventory_item(product_id))
    
    inventory_ids = [item["inventory_id"] for item in inventory_items]
    
    # Generate sales data
    sales_data = []
    for product_id in product_ids:
        for _ in range(random.randint(5, 15)):
            sales_data.append(generate_sales_data(product_id))
    
    # Generate logistics data
    logistics_data = []
    for i in range(min(len(product_ids), len(inventory_ids))):
        for _ in range(random.randint(1, 5)):
            logistics_data.append(generate_logistics_data(
                product_ids[i % len(product_ids)], 
                inventory_ids[i % len(inventory_ids)]
            ))
    
    # Wrap data according to the expected schema
    upload_data = {
        "title": "Sample Data Upload",
        "description": "Auto-generated test data for development",
        "data": {
            "products": products,
            "inventory": inventory_items,
            "sales": sales_data,
            "logistics": logistics_data
        }
    }
    
    # Upload data
    try:
        response = requests.post(f"{base_url}/api/v1/data/upload", json=upload_data)
        print(f"Data upload status: {response.status_code}")
        if response.status_code in [200, 201]:
            print("Sample data uploaded successfully")
            return response.json()
        else:
            print(f"Error uploading data: {response.text}")
            return None
    except Exception as e:
        print(f"Exception during data upload: {str(e)}")
        return None


# ------------------- Forecast Section -------------------
def train_forecast_model():
    # Parameters for training the forecasting model
    training_params = {
        "algorithm": random.choice(["ARIMA", "Prophet", "LSTM", "XGBoost"]),
        "historical_periods": random.randint(6, 24),
        "forecast_horizon": random.randint(3, 12),
        "features": ["historical_sales", "seasonality", "price_elasticity", "marketing_events"],
        "cross_validation": True,
        "validation_method": "time_series_split"
    }
    
    try:
        response = requests.post(f"{base_url}/api/v1/forecast/train", json=training_params)
        print(f"Forecast model training status: {response.status_code}")
        if response.status_code == 200:
            print("Forecast model training initiated")
            return response.json()
        else:
            print(f"Error training model: {response.text}")
            return None
    except Exception as e:
        print(f"Exception during model training: {str(e)}")
        return None

def refine_forecast_model():
    # Parameters for refining the forecasting model
    refinement_params = {
        "model_id": generate_id(),  # Would use a real model ID in practice
        "adjustments": {
            "seasonality_strength": random.uniform(0.1, 1.0),
            "trend_dampening": random.uniform(0.1, 0.9),
            "outlier_detection": random.choice([True, False]),
            "special_events": [
                {
                    "name": "Holiday Season",
                    "start_date": "2024-11-25",
                    "end_date": "2024-12-31",
                    "expected_lift": random.uniform(1.2, 2.5)
                },
                {
                    "name": "Summer Sale",
                    "start_date": "2024-07-01",
                    "end_date": "2024-07-15",
                    "expected_lift": random.uniform(1.1, 1.8)
                }
            ]
        }
    }
    
    try:
        response = requests.post(f"{base_url}/api/v1/forecast/refine", json=refinement_params)
        print(f"Forecast model refinement status: {response.status_code}")
        if response.status_code == 200:
            print("Forecast model refinement initiated")
            return response.json()
        else:
            print(f"Error refining model: {response.text}")
            return None
    except Exception as e:
        print(f"Exception during model refinement: {str(e)}")
        return None

# ------------------- Supplier Section -------------------
def generate_supplier():
    return {
        "supplier_id": generate_id(),
        "name": fake.company(),
        "contact_person": fake.name(),
        "email": fake.company_email(),
        "phone": fake.phone_number(),
        "address": {
            "street": fake.street_address(),
            "city": fake.city(),
            "state": fake.state(),
            "zip": fake.zipcode(),
            "country": fake.country()
        },
        "category": random.choice(["Raw Materials", "Finished Goods", "Services", "Equipment"]),
        "rating": round(random.uniform(1.0, 5.0), 1),
        "active": random.choice([True, False]),
        "onboarded_date": fake.date_this_decade().isoformat()
    }

def create_suppliers(count=10):
    suppliers = []
    for _ in range(count):
        supplier = generate_supplier()
        try:
            response = requests.post(f"{base_url}/api/v1/suppliers", json=supplier)
            print(f"Supplier creation response: {response.status_code} - {response.text}")
            if response.status_code in [200, 201]:  # Handle both 200 and 201 status codes
                created_supplier = response.json()
                supplier_id = created_supplier.get("supplier_id") or supplier["supplier_id"]
                if supplier_id:
                    print(f"Created supplier: {supplier['name']} with ID: {supplier_id}")
                    supplier["supplier_id"] = supplier_id  # Ensure the supplier has an ID
                    suppliers.append(supplier)
                else:
                    print(f"Error: Supplier ID missing in response: {response.text}")
            else:
                print(f"Error creating supplier: {response.text}")
        except Exception as e:
            print(f"Exception creating supplier: {str(e)}")
    
    return suppliers

def generate_inventory_item_for_supplier(supplier_id):
    return {
        "item_id": generate_id(),
        "supplier_id": supplier_id,
        "name": f"{fake.word().capitalize()} {random.choice(['Component', 'Material', 'Part', 'Supply', 'Kit'])}",
        "sku": fake.bothify(text='ITEM-####-????'),
        "category": random.choice(["Raw Material", "Component", "Packaging", "Finished Good"]),
        "unit_price": round(random.uniform(1.0, 500.0), 2),
        "minimum_order_quantity": random.randint(1, 100),
        "lead_time_days": random.randint(1, 60),
        "current_stock": random.randint(0, 1000),
        "reorder_point": random.randint(10, 200),
        "created_at": fake.date_time_this_year().isoformat()
    }

def create_supplier_items(suppliers, items_per_supplier=5):
    items = []
    for supplier in suppliers:
        supplier_id = supplier.get("supplier_id", supplier.get("id"))
        for _ in range(items_per_supplier):
            item = generate_inventory_item_for_supplier(supplier_id)
            try:
                response = requests.post(f"{base_url}/api/v1/suppliers/inventory/items", json=item)
                if response.status_code == 201:
                    print(f"Created item: {item['name']}")
                    items.append(response.json())
                else:
                    print(f"Error creating item: {response.text}")
            except Exception as e:
                print(f"Exception creating item: {str(e)}")
    
    return items

def restock_items(items, restock_count=10):
    if not items:
        print("No items available for restocking.")
        return

    for _ in range(restock_count):
        item = random.choice(items)
        item_id = item.get("item_id", item.get("id"))
        restock_data = {
            "item_id": item_id,
            "quantity": random.randint(10, 500),
            "purchase_price": round(random.uniform(item.get("unit_price", 10) * 0.8, 
                                                  item.get("unit_price", 10) * 1.2), 2),
            "delivery_date": fake.future_date().isoformat(),
            "purchase_order_number": fake.bothify(text='PO-########'),
            "notes": fake.text(max_nb_chars=100)
        }
        
        try:
            response = requests.post(f"{base_url}/api/v1/suppliers/inventory/restock", json=restock_data)
            if response.status_code == 200:
                print(f"Restocked item: {item_id}")
            else:
                print(f"Error restocking item: {response.text}")
        except Exception as e:
            print(f"Exception restocking item: {str(e)}")

# ------------------- AI Models Section -------------------
def train_ai_model():
    model_types = ["Demand Forecasting", "Price Optimization", "Inventory Management", 
                   "Supplier Selection", "Logistics Optimization"]
    algorithms = ["Random Forest", "Gradient Boosting", "Neural Network", "LSTM", "Prophet"]
    
    training_data = {
        "title": f"{random.choice(model_types)} - {random.choice(algorithms)}",
        "description": fake.text(max_nb_chars=200),
        "data": {
            "features": random.sample(["historical_sales", "seasonality", "price", "promotions", 
                                       "holidays", "weather", "competitor_prices", "stock_levels", 
                                       "supplier_performance", "lead_times"], 
                                      k=random.randint(3, 7)),
            "target_variable": random.choice(["demand", "optimal_price", "reorder_point", 
                                              "supplier_rating", "delivery_time"]),
            "training_size": random.uniform(0.6, 0.8),
            "validation_size": random.uniform(0.1, 0.2),
            "hyperparameters": {
                "learning_rate": random.uniform(0.001, 0.1),
                "max_depth": random.randint(3, 10),
                "num_estimators": random.randint(50, 500),
                "regularization": random.uniform(0.01, 0.5)
            }
        }
    }
    
    try:
        response = requests.post(f"{base_url}/api/v1/ai/models/train", json=training_data)
        print(f"AI model training status: {response.status_code}")
        if response.status_code in [200, 201]:  # Handle both 200 and 201 status codes
            print("AI model training initiated")
            return response.json()
        else:
            print(f"Error training AI model: {response.text}")
            return None
    except Exception as e:
        print(f"Exception during AI model training: {str(e)}")
        return None

# ------------------- Tracking Section -------------------
def generate_order():
    statuses = ["Processing", "Shipped", "In Transit", "Delivered", "Delayed", "Returned"]
    return {
        "order_id": generate_id(),
        "customer_id": generate_id(),
        "order_date": fake.date_time_this_month().isoformat(),
        "status": random.choice(statuses),
        "shipping_address": {
            "street": fake.street_address(),
            "city": fake.city(),
            "state": fake.state(),
            "zip": fake.zipcode(),
            "country": fake.country()
        },
        "items": [
            {
                "product_id": generate_id(),
                "quantity": random.randint(1, 10),
                "price": round(random.uniform(10.0, 500.0), 2)
            } for _ in range(random.randint(1, 5))
        ],
        "shipping_method": random.choice(["Standard", "Express", "Next Day", "International"]),
        "tracking_number": fake.bothify(text='TRK-####-####-####'),
        "estimated_delivery": fake.future_date().isoformat(),
        "actual_delivery": fake.date_time_this_month().isoformat() if random.random() > 0.5 else None
    }

def create_orders(count=20):
    orders = []
    for _ in range(count):
        order = generate_order()
        try:
            # In a real scenario, you would POST this to create an order
            # For this demo, we're just adding it to our list
            orders.append(order)
            print(f"Created order: {order['order_id']}")
        except Exception as e:
            print(f"Exception creating order: {str(e)}")
    
    return orders

def update_order_status(orders, update_count=10):
    for _ in range(update_count):
        if not orders:
            break
            
        order = random.choice(orders)
        new_status = random.choice(["Processing", "Shipped", "In Transit", "Delivered", "Delayed", "Returned"])
        update_data = {
            "order_id": order["order_id"],
            "status": new_status,
            "updated_at": fake.date_time_this_month().isoformat(),
            "notes": fake.text(max_nb_chars=100),
            "location": fake.city() if new_status in ["Shipped", "In Transit"] else None,
            "estimated_delivery": fake.future_date().isoformat() if new_status != "Delivered" else None,
            "actual_delivery": fake.date_time_this_month().isoformat() if new_status == "Delivered" else None
        }
        
        try:
            response = requests.post(f"{base_url}/api/v1/tracking/update", json=update_data)
            if response.status_code == 200:
                print(f"Updated order {order['order_id']} to status: {new_status}")
            else:
                print(f"Error updating order: {response.text}")
        except Exception as e:
            print(f"Exception updating order: {str(e)}")

# ------------------- Main Execution -------------------
def main():
    print("Starting data population process...")
    
    # Skip clearing existing data since it's failing
    print("Skipping data clearing due to backend error...")
    
    # Upload core data (products, inventory, sales, logistics)
    uploaded_data = upload_sample_data()
    
    if uploaded_data:
        # Continue with the rest of the operations only if data upload was successful
        # Create suppliers and their items
        suppliers = create_suppliers(count=10)
        items = create_supplier_items(suppliers, items_per_supplier=5)
        restock_items(items, restock_count=15)
        
        # Train forecasting model
        trained_forecast = train_forecast_model()
        if trained_forecast:
            refine_forecast_model()
        
        # Train AI models
        for _ in range(3):
            train_ai_model()
        
        # Create and update orders
        orders = create_orders(count=25)
        update_order_status(orders, update_count=15)
    
    print("Data population completed!")

if __name__ == "__main__":
    main()