from abc import ABC, abstractmethod

from core.datasource_id import DataSourceId


class DataSourceIdProvider(ABC):
    @abstractmethod
    def get_id(self) -> DataSourceId:
        pass

class DataSourceIdProviderRegistry():
    def get(self, type: str, args) -> DataSourceIdProvider:
        registry = dict()
        registry["list"] = lambda config: ListBasedSourceIdProvider(config["ids"])
        #registry["gradual"] = lambda config: DataSourceIdProvider(config["tickCount"], config["minimalLoad"], config["maximalLoad"])
        return registry[type](args)

class NumberDataSourceIdProvider(DataSourceIdProvider):

    def __init__(self):
        self.id = 0

    def get_id(self) -> DataSourceId:
        data_source_id = DataSourceId(str(self.id))
        self.id += 1
        return data_source_id


class ListBasedSourceIdProvider(DataSourceIdProvider):

    def __init__(self, id_list):
        self.id_list = id_list
        self.pointer = 0

    def get_id(self) -> DataSourceId:
        data_source_id = DataSourceId(str(self.id_list[self.pointer]))
        self.pointer += 1
        return data_source_id
