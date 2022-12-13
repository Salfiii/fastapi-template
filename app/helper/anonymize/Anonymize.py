import warnings
import pandas as pd
from nested_lookup import nested_alter, nested_delete, nested_update


class Anonymize:
    """
    Remove or alter some parts of the given data to anonymize it
    
    Attributes:
        data (object): The data object to anonymize
        strip (list): elements/columns to strip from data
        hard_delete(bool): If true, deletes the element/node, otherwise overwrites the value with "overwrite_value"
        overwrite_value (str): Value to overwrite elements/nodes if "hard_delete" is False.
        change: elements/columns an the corresponding change action
            Change needs to be provided in the following format:
            [
                [
                ["plz", "postalcode"] # Elements to process 
                ch_postal_code, # change function which handles a scalar value
                [5,True,1,0], # parameters of the change function
                str # pre-processing function for the scalar value before it goes into the change function
                ],
                [...] # another configuration.
            ]
        wild_change (bool): if wild is True, treat the given key as a case insensitive substring when performing lookups.
        allowed_classes (list): defines which classes are allow in the anon.-process. 
    """

    def __init__(self, strip: list = None, hard_delete: bool = True, overwrite_value: str = None,
                 change: list = None, wild_change: bool = False):
        """   
        Args:
            strip (list): elements/columns to strip from data
                Defaults to None.
            hard_delete(bool): If true, deletes the element/node, otherwise overwrites the value with "overwrite_value"
                Defaults to True.
            overwrite_value (str): Value to overwrite elements/nodes if "hard_delete" is False.
                Defaults to None.
            change (list): elements/columns an the corresponding change action @TODO
                Defaults to None.
            wild_change (bool): if wild is True, treat the given key as a case insensitive substring when performing lookups.
                Defaults to False
    
        """
        self.strip = strip
        self.hard_delete = hard_delete
        self.overwrite_value = overwrite_value
        self.change = change
        self.wild_change = wild_change
        self.allowed_classes = [dict, pd.core.frame.DataFrame, list]

    def perform_anonymization(self, data: object):
        """
        Performs multiple anonymization tasks on the data

        Args:
            data (object):The data object to anonymize

        Returns:
            [dict, pd.core.frame.DataFrame, list]
            Returns the data in the provided structure
        """
        object_type = type(data)
        possible = True if object_type in self.allowed_classes else False
        anon_data = None

        if possible:
            if object_type in [dict, list]:
                anon_data = self.__anon_dict(data)
            elif object_type == pd.core.frame.DataFrame:
                anon_data = self.__anon_dataframe(data)
            else:
                warnings.warn("Data of type/class " + object_type + " is currently not supported."
                              "This Statement should not be reachable, please contact a developer")
        else:
            warnings.warn("Data of type/class " + object_type + " is currently not supported")

        return anon_data

    def __anon_dict(self, data: object) -> [dict]:
        """
        Anonymizes (Removes, alters) given parts of a dict or a list of dicts

        Returns:
            [dict, list[dict]]
            If only a single dict was provided, a dict will be returned, otherwise a list of dicts.

        """
        # If a list is provided, check the first element is a dict and asume
        # that all other elements are dicts too.
        if type(data) == list:
            elem_to_check = data[0]
            is_list_of_dicts = type(elem_to_check) == dict
            if is_list_of_dicts == False:
                warnings.warn("You provided a list which did not only hold dict-objects."
                              "Please remove all other objects except dicts from the list")
                return None
        else:
            is_list_of_dicts = False

        # local anon function for one dict
        def _anon_dict_strip_intern(data: object):
            """
            @TODO
            """
            ret = data
            # Check if any strip values are provided
            if self.strip != None:
                # Iterate over the elements to strip.
                for val in self.strip:
                    # if hard_delete is True, delete the node/element, else overwrite it.
                    if self.hard_delete:
                        ret = nested_delete(data, val, in_place=True)
                    else:
                        ret = nested_update(data, val, self.overwrite_value, in_place=True)
            return ret

        def _anon_dict_alter_intern(data: object, config_list: list = None):
            """
            @TODO
            """
            # print("altering:....")
            # exit early if no config is provided
            if config_list is None:
                return data

            # iterate over the config and extract the pieces
            for conf in config_list:
                element = conf[0]  # list of names of the dict elements to be altered
                func = conf[1]  # function to process those elements
                try:
                    func_params = conf[
                        2]  # arguments of those functions. Optional, try assures that no error is thrown in absence
                except:
                    func_params = None
                try:
                    conv_func = conf[3]  # possible conversion function like 'str'
                except:
                    conv_func = None

                # loop over all given names which should be altered
                for ele in element:
                    data = nested_alter(document=data, key=ele, callback_function=func,
                                        function_parameters=func_params, conversion_function=conv_func,
                                        wild_alter=self.wild_change)

            return data

        ret = list()
        # iterate over list or just use the on provided dict
        if is_list_of_dicts:
            for elem in data:
                ret.append(
                    # delte/update all strip-elements
                    _anon_dict_strip_intern(
                        # process the change-elements
                        _anon_dict_alter_intern(elem, self.change)
                    )
                )
        else:
            # delte/update all strip-elements
            ret = _anon_dict_strip_intern(
                # process the change-elements
                _anon_dict_alter_intern(data, self.change)
            )

        return ret

    def __anon_dataframe(self, data: object) -> pd.DataFrame:
        """
        Anonymizes (Removes, alters) given parts of a pd.core.frame.DataFrame

        Returns:
            pandas.core.frame.DataFrame
        """
        # Check if any strip values are provided
        if self.strip != None:
            # if hard_delete is True, delete the node/element, else overwrite it.
            if self.hard_delete:
                data = pd.DataFrame(data).drop(labels=self.strip, axis=1)
            else:
                data[self.strip] = self.overwrite_value

        return data
