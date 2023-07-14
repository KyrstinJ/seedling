from typing import List
from bson import ObjectId
from models import GardenIn, GardenOut
from queries.client import Queries


class GardenRepository(Queries):
    DB_NAME = "db-seedling-db"
    COLLECTION = "gardens"
    PLANT_COLLECTION = "plants"

    def create(self, garden: GardenIn) -> GardenOut:
        garden = garden.dict()
        self.collection.insert_one(garden)
        garden["id"] = str(garden["_id"])
        return GardenOut(**garden)

    def get_all(self) -> List[GardenOut]:
        gardens = self.collection.find()
        gardensPropsList = list(gardens)
        for gardenProps in gardensPropsList:
            gardenProps["id"] = str(gardenProps["_id"])
        return [GardenOut(**garden) for garden in gardensPropsList]

    def get_one(self, garden_id: str) -> GardenOut:
        garden = self.collection.find_one({"_id": ObjectId(garden_id)})
        garden["id"] = str(garden["_id"])
        return GardenOut(**garden)

    def delete(self, garden_id: str):
        self.collection.delete_one(
            {
                "_id": ObjectId(garden_id),
            }
        )
