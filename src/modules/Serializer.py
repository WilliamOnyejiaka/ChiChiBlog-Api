from typing import Dict,List


class Serializer:

    needed_attributes:List = []

    def __init__(self,needed_attributes:List):
        self.needed_attributes = needed_attributes

    def serialize(self, data:Dict) -> Dict:
        result:Dict = {}
        for attr in self.needed_attributes:
            if attr == '_id':
                result[attr] = str(data[attr])
            else:
                result[attr] = data[attr]
        return result

    def dump(self,data_list):
        result:List = []
        for index in range(len(data_list)):
            data = self.serialize(data_list[index])
            result.append(data)
        return result
        
    def dump_find(self,documents) -> List:
        data = []
        for document in documents:
            for attr in self.needed_attributes:
                if attr == '_id':
                    document[attr] = str(document[attr])
                else:
                    document[attr] = document[attr]
            data.append(document)
        return data