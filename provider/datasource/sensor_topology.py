from abc import ABC, abstractmethod
from typing import List

from core.datasource import DataSource, GenericDataSource, StartDataSource, EndDataSource
from core.datasource_id import START_SENSOR_ID, END_DATA_SOURCE_ID
from provider.activity.selection.activity_selection_provider import ActivitySelectionProviderFactory
from provider.datasource.datasource_id_provider import DataSourceIdProvider
from provider.sink.console.console_sink import PrintConsoleSinkProvider
from provider.sink.sink_provider import SinkProvider
from provider.transition.duration.duration_provider import DurationProvider
from provider.transition.nextsensor.next_sensor_provider import NextSensorProvider
from provider.transition.transition_provider_factory import MatrixBasedTransitionProvider


class DataSourceTopologyProvider:
    @abstractmethod
    def get_sensor_topology(self, number_of_sensors) -> List[DataSource]:
        pass


class ConcreteDataSourceTopologyProvider(DataSourceTopologyProvider):
    def __init__(self, data_source_list: List[DataSource]):
        self.data_source_list = data_source_list

    def get_sensor_topology(self, number_of_sensors):
        data_sources = []
        transitions = [0.0] * number_of_sensors
        transitions[0] = 1.0
        data_sources.append(
            StartDataSource(
                transition_provider=NextSensorProvider(transitions),
                sender=PrintConsoleSinkProvider().get_sender(START_SENSOR_ID.get_name())))
        for data_source in self.data_source_list:
            data_sources.append(data_source)

        data_sources.append(EndDataSource(sender=PrintConsoleSinkProvider().get_sender(END_DATA_SOURCE_ID.get_name())))
        return data_sources
