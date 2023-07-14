from pydantic import BaseModel, HttpUrl
from typing import List
from queries.database import db
from bson import ObjectId
from models import Error, GardenOut


class PlantIn(BaseModel):
    name: str
    plant_picture: HttpUrl
    garden_id: str


class PlantOut(BaseModel):
    id: str
    name: str
    plant_picture: HttpUrl
    garden: GardenOut


class PlantRepository:
    plants_collection = db.plants
    gardens_collection = db.gardens

    def create(self, plant: PlantIn) -> PlantOut:
        try:
            garden = self.gardens_collection.find_one(
                {"_id": ObjectId(plant.garden_id)}
            )
            if garden:
                garden_info = GardenOut(
                    id=str(garden["_id"]),
                    name=garden["name"],
                    location=garden["location"],
                )
                result = self.plants_collection.insert_one(
                    {**plant.dict(), "garden_id": garden_info.id}
                )
                inserted_id = str(result.inserted_id)
                return PlantOut(
                    id=inserted_id,
                    name=plant.name,
                    garden=garden_info,
                    plant_picture=plant.plant_picture,
                )
            else:
                return Error(message="Invalid Garden Name")
        except Exception as e:
            error_message = str(e)
            return Error(message=error_message)

    def get_all(self) -> List[PlantOut]:
        try:
            plants = []
            for plant in self.plants_collection.find().sort("name"):
                garden_id = plant["garden_id"]
                garden = self.gardens_collection.find_one(
                    {"_id": ObjectId(garden_id)}
                )
                if garden:
                    garden_info = GardenOut(
                        id=str(garden["_id"]),
                        name=garden["name"],
                        location=garden["location"],
                    )
                    plant_info = PlantOut(
                        id=str(plant["_id"]),
                        name=plant["name"],
                        garden=garden_info,
                        plant_picture=plant["plant_picture"],
                    )
                    plants.append(plant_info)
            return plants
        except Exception as e:
            error_message = str(e)
            return Error(message=error_message)

    def get_one(self, plant_id: str) -> PlantOut:
        try:
            plant = self.plants_collection.find_one(
                {"_id": ObjectId(plant_id)}
            )
            if plant is None:
                return None
            garden_id = plant["garden_id"]
            garden = self.gardens_collection.find_one(
                {"_id": ObjectId(garden_id)}
            )
            if garden is None:
                return None
            garden_info = GardenOut(
                id=str(garden["_id"]),
                name=garden["name"],
                location=garden["location"],
            )
            return PlantOut(
                id=str(plant["_id"]),
                name=plant["name"],
                garden=garden_info,
                plant_picture=plant["plant_picture"],
            )
        except Exception as e:
            error_message = str(e)
            return Error(message=error_message)

    def delete(self, plant_id: str) -> bool:
        try:
            result = self.plants_collection.delete_one(
                {"_id": ObjectId(plant_id)}
            )
            return result.deleted_count == 1
        except Exception as e:
            error_message = str(e)
            return Error(message=error_message)
