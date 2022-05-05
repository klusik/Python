class Helper:
    """ Stuff that helps """
    @staticmethod
    def dict_dump(variable, # variable which is readed
                  indent=0, # indent of the print
                  indent_symbol = ' ', # symbol of the indent, default ' '
                  ):
        """ Dumps variable in readable way """

        # Assuming the 'variable' is dict and its all items
        # are values or dicts.

        for index, item in enumerate(variable.items()):
            print(f"{str(indent_symbol)*indent}{item[0]}")
            if isinstance(item[1], dict):
                Helper.dict_dump(item[1], indent+1, ' ')
            else:
                print(f"{str(indent_symbol)*(indent+1)}{item[1]}")

