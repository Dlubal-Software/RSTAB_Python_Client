import enum
from RSTAB.initModel import Model
from RSTAB.enums import CaseObjectType, ObjectTypes
from RSTAB.dataTypes import inf

# We  can't extract lines with description: Extremes, Total, and Average. Those are language dependent.
# To do it set_settings_program_language() has to be called before calculation and the program needs to be restarted.

def GetResultTableParameters(results):
    '''
    Returns dict with 3 atributes: base, row and error.
    '''
    params = {'base':[], 'row':[], 'error': None}

    if not results:
        return ''

    if results[0][0]:
        for i in results[0]:
            params['base'] = list(set(params['base'] + i.__keylist__))
            if 'row' in i.__keylist__ and i.row:
                params['row'] = list(set(params['row'] + i.row.__keylist__))
            else:
                params['errors'] = "Result table doesn't have attribute 'row'."

    return params


def ConvertResultsToListOfDct(results, includeBase = False):
    '''
    Args:
        results (ResultTables class): ResultTables object
        includeBase (bool): Include base information of every line. Typicaly 'object number' and 'description'. Default is False.
    Returns:
        List of dictionaries. Each dictionary corresponds to one line in result table.
    '''
    if not results:
        return ''

    params = GetResultTableParameters(results)
    lstOfDct = []

    for r in results[0]:
        dct = {}
        if includeBase and params['base']:
            for i in params['base']:
                if i == 'row':
                    for y in params['row']:
                        # Sometimes the parameters are not in table or
                        # they are defined by type+value structure called 'variant',
                        # hence using try-except notation
                        try:
                            dct[y] = float(r.row[y].value)
                        except:
                            try:
                                dct[y] = r.row[y].value
                            except:
                                try:
                                    dct[y] = float(r.row[y])
                                except:
                                    try:
                                        dct[y] = r.row[y]
                                    except:
                                        pass
                else:
                    try:
                        dct[i] = float(r[i])
                    except:
                        try:
                            dct[i] = r[i]
                        except:
                            pass
            lstOfDct.append(dct)
        # include only row
        else:
            if params['row']:
                for i in params['row']:
                    try:
                        dct[i] = float(r.row[i].value)
                    except:
                        try:
                            dct[i] = r.row[i].value
                        except:
                            try:
                                dct[i] = float(r.row[i])
                            except:
                                try:
                                    dct[i] = r.row[i]
                                except:
                                    pass
                lstOfDct.append(dct)

    if params['error']:
        return lstOfDct.append({'error': params['error']})

    return lstOfDct


def GetMinValue(structured_results, parameter):

    '''
    Args:
        structured_results(list of dicts): Result of ConvertResultsToListOfDct() function
        parameter(str, mandatory): The parameter for which the minimum is sought.
    '''

    min_val = inf
    for i in structured_results:
        # Sometimes there is text where the float should be
        try:
            min_val = min(float(i[parameter]), min_val)
        except:
            pass

    assert min_val < inf, 'Check if the parameter is in the table.'

    return min_val


def GetMaxValue(structured_results, parameter):

    '''
    Args:
        structured_results(list of dicts): Result of ConvertResultsToListOfDct() function
        parameter(str, mandatory): The parameter for which the maximum is sought.
    '''

    max_val = -inf
    for i in structured_results:
        # Sometimes there is text where the float should be
        try:
            max_val = max(float(i[parameter]), max_val)
        except:
            pass

    assert max_val > -inf, 'Check if the parameter is in the table.'

    return max_val


def CreateObjectLocation(
    object_type = 'E_OBJECT_TYPE_NODE',
    object_no = 1,
    model = Model):

    if object_no > 0:
        object_locations = model.clientModel.factory.create('ns0:object_location_array')

        object = model.clientModel.factory.create('ns0:object_location')
        object.type = object_type
        object.no = object_no
        object_locations.object_location.append(object)

        return object_locations
    else:
        return None


class ResultTables():


    @staticmethod
    def BuildingStoriesForcesInShearWalls(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Object number
            model (class, optional): Model instance
        '''

        results = model.clientModel.service.get_results_for_building_stories_forces_in_shear_walls(
            loading_type.name,
            loading_no,
            object_locations = None # TODO: add filtering by Shear Wall number
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def BuildingStoriesCentresMassRigidity(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Object number
            model (class, optional): Model instance
        '''

        results = model.clientModel.service.get_results_for_building_stories_centres_mass_rigidity(
            loading_type.name,
            loading_no,
            object_locations = None  # TODO: add filtering by Story number
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def BuildingStoriesInterstoryDrifts(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Object number
            model (class, optional): Model instance
        '''

        results = model.clientModel.service.get_results_for_building_stories_interstory_drifts(
            loading_type.name,
            loading_no,
            object_locations = None  # TODO: add filtering by Story number
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def BuildingStoriesStoryActions(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Object number
            model (class, optional): Model instance
        '''

        results = model.clientModel.service.get_results_for_building_stories_story_actions(
            loading_type.name,
            loading_no,
            object_locations = None  # TODO: add filtering by Story number
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def CalculationDiagrams(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Object number
            model (class, optional): Model instance
        '''

        results = model.clientModel.service.get_results_for_calculation_diagrams(
            loading_type.name,
            loading_no,
            object_locations = None
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def CriticalLoadFactors(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Object number
            model (class, optional): Model instance
        '''

        results = model.clientModel.service.get_results_for_critical_load_factors(
            loading_type.name,
            loading_no,
            object_locations = None  # TODO: add filtering by mode shape number
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def EffectiveLengthsAndCriticalLoadsByEigenvector(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Object number
            model (class, optional): Model instance
        '''

        results = model.clientModel.service.get_results_for_effective_lengths_and_critical_loads_by_eigenvector(
            loading_type.name,
            loading_no,
            object_locations = None  # TODO: add filtering by mode shape number
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def EffectiveLengthsAndCriticalLoadsByMember(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_effective_lengths_and_critical_loads_by_member(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def EigenvectorsByMember(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_eigenvectors_by_member(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def EigenvectorsByNode(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Node number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_NODE.name, object_no)

        results = model.clientModel.service.get_results_for_eigenvectors_by_node(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def Errors(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Object number
            model (class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_errors(loading_type.name, loading_no, object_no), include_base)


    @staticmethod
    def MembersByEigenvector(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_members_by_eigenvector(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def MembersContactForces(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_members_contact_forces(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def MembersGlobalDeformations(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_members_global_deformations(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def MembersHingeDeformations(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_members_hinge_deformations(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def MembersHingeForces(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_members_hinge_forces(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def MembersInternalForces(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_members_internal_forces(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def MembersInternalForcesByMemberSet(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member Set number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER_SET.name, object_no)

        results = model.clientModel.service.get_results_for_members_internal_forces_by_member_set(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def MembersInternalForcesByCrossSection(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Section number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_CROSS_SECTION.name, object_no)

        results = model.clientModel.service.get_results_for_members_internal_forces_by_section(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def MembersLocalDeformations(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_members_local_deformations(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def MembersStrains(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        without_extremes: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_members_strains(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def ModalAnalysisEffectiveModalMasses(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Object number
            model (class, optional): Model instance
        '''

        results = model.clientModel.service.get_results_for_modal_analysis_effective_modal_masses(
            loading_type.name,
            loading_no,
            object_locations = None # TODO: add filtering by mode shape number
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def ModalAnalysisMassesInLocations(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Object number
            model (class, optional): Model instance
        '''

        results = model.clientModel.service.get_results_for_modal_analysis_effective_modal_masses(
            loading_type.name,
            loading_no,
            object_locations = None # TODO: add filtering by mesh point number
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def ModalAnalysisMembersByModeShape(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_modal_analysis_members_by_mode_shape(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def ModalAnalysisModeShapesByMember(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_modal_analysis_mode_shapes_by_member(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def ModalAnalysisModeShapesByNode(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Node number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_NODE.name, object_no)

        results = model.clientModel.service.get_results_for_modal_analysis_mode_shapes_by_node(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def ModalAnalysisNaturalFrequencies(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Object number
            model (class, optional): Model instance
        '''

        results = model.clientModel.service.get_results_for_modal_analysis_natural_frequencies(
            loading_type.name,
            loading_no,
            object_locations = None # add filtering by mode shape number ?
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def ModalAnalysisNodesByModeShape(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Node number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_NODE.name, object_no)

        results = model.clientModel.service.get_results_for_modal_analysis_nodes_by_mode_shape(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def ModalAnalysisParticipationFactors(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Object number
            model (class, optional): Model instance
        '''

        results = model.clientModel.service.get_results_for_modal_analysis_participation_factors(
            loading_type.name,
            loading_no,
            object_locations = None # add filtering by mode shape number ?
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def NodesByEigenvector(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Node number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_NODE.name, object_no)

        results = model.clientModel.service.get_results_for_nodes_by_eigenvector(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def NodesDeformations(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Node number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_NODE.name, object_no)

        results = model.clientModel.service.get_results_for_nodes_deformations(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def NodesSupportForces(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Node number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_NODE.name, object_no)

        results = model.clientModel.service.get_results_for_nodes_support_forces(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def SpectralAnalysisBuildingStoriesCentresMassRigidity(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Object number
            model (class, optional): Model instance
        '''

        results = model.clientModel.service.get_results_for_spectral_analysis_building_stories_centres_mass_rigidity(
            loading_type.name,
            loading_no,
            object_locations = None  # todo: add filtering by Story number
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def SpectralAnalysisBuildingStoriesForcesInShearWalls(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Object number
            model (class, optional): Model instance
        '''

        results = model.clientModel.service.get_results_for_spectral_analysis_building_stories_forces_in_shear_walls(
            loading_type.name,
            loading_no,
            object_locations = None  # todo: add filtering by Shear Wall number
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def SpectralAnalysisBuildingStoriesInterstoryDrifts(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Object number
            model (class, optional): Model instance
        '''

        results = model.clientModel.service.get_results_for_spectral_analysis_building_stories_interstory_drifts(
            loading_type.name,
            loading_no,
            object_locations = None  # todo: add filtering by Story number
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def SpectralAnalysisBuildingStoriesStoryActions(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Object number
            model (class, optional): Model instance
        '''

        results = model.clientModel.service.get_results_for_spectral_analysis_building_stories_story_actions(
            loading_type.name,
            loading_no,
            object_locations = None  # todo: add filtering by Story number
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def SpectralAnalysisMembersContactForces(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_spectral_analysis_members_contact_forces(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def SpectralAnalysisMembersGlobalDeformations(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_spectral_analysis_members_global_deformations(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def SpectralAnalysisMembersHingeDeformations(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_spectral_analysis_members_hinge_deformations(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def SpectralAnalysisMembersHingeForces(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_spectral_analysis_members_hinge_forces(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def SpectralAnalysisMembersInternalForces(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_spectral_analysis_members_internal_forces(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def SpectralAnalysisMembersInternalForcesByMemberSet(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member Set number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER_SET.name, object_no)

        results = model.clientModel.service.get_results_for_spectral_analysis_members_internal_forces_by_member_set(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def SpectralAnalysisMembersInternalForcesByCrossSection(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Section number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_CROSS_SECTION.name, object_no)

        results = model.clientModel.service.get_results_for_spectral_analysis_members_internal_forces_by_section(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def SpectralAnalysisMembersLocalDeformations(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_spectral_analysis_members_local_deformations(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def SpectralAnalysisMembersStrains(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_spectral_analysis_members_strains(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def SpectralAnalysisNodesDeformations(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Node number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_NODE.name, object_no)

        results = model.clientModel.service.get_results_for_spectral_analysis_nodes_deformations(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def SpectralAnalysisNodesPseudoAccelerations(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Node number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_NODE.name, object_no)

        results = model.clientModel.service.get_results_for_spectral_analysis_nodes_pseudo_accelerations(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def SpectralAnalysisNodesPseudoVelocities(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Node number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_NODE.name, object_no)

        results = model.clientModel.service.get_results_for_spectral_analysis_nodes_pseudo_velocities(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def SpectralAnalysisNodesSupportForces(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Node number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_NODE.name, object_no)

        results = model.clientModel.service.get_results_for_spectral_analysis_nodes_support_forces(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def SpectralAnalysisSummary(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Object number
            model (class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_spectral_analysis_summary(loading_type.name, loading_no, object_no), include_base)


    @staticmethod
    def StabilityIncrementalAnalysisBuildingStoriesCentresMassRigidity(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Object number
            model (class, optional): Model instance
        '''

        results = model.clientModel.service.get_results_for_stability_incremental_analysis_building_stories_centres_mass_rigidity(
            loading_type.name,
            loading_no,
            object_locations = None # TODO: add filtering by Story number
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def StabilityIncrementalAnalysisBuildingStoriesForcesInShearWalls(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Object number
            model (class, optional): Model instance
        '''

        results = model.clientModel.service.get_results_for_stability_incremental_analysis_building_stories_forces_in_shear_walls(
            loading_type.name,
            loading_no,
            object_locations = None # TODO: add filtering by Shear Wall number
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def StabilityIncrementalAnalysisBuildingStoriesInterstoryDrifts(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Object number
            model (class, optional): Model instance
        '''

        results = model.clientModel.service.get_results_for_stability_incremental_analysis_building_stories_interstory_drifts(
            loading_type.name,
            loading_no,
            object_locations = None # TODO: add filtering by Story number
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def StabilityIncrementalAnalysisBuildingStoriesStoryActions(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Object number
            model (class, optional): Model instance
        '''

        results = model.clientModel.service.get_results_for_stability_incremental_analysis_building_stories_story_actions(
            loading_type.name,
            loading_no,
            object_locations = None # TODO: add filtering by Story number
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def StabilityIncrementalAnalysisCalculationDiagrams(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Object number
            model (class, optional): Model instance
        '''

        results = model.clientModel.service.get_results_for_stability_incremental_analysis_calculation_diagrams(
            loading_type.name,
            loading_no,
            object_locations = None # TODO: add filtering by ?
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def StabilityIncrementalAnalysisMembersContactForces(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_stability_incremental_analysis_members_contact_forces(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def StabilityIncrementalAnalysisMembersGlobalDeformations(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_stability_incremental_analysis_members_global_deformations(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def StabilityIncrementalAnalysisMembersHingeDeformations(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_stability_incremental_analysis_members_hinge_deformations(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def StabilityIncrementalAnalysisMembersHingeForces(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_stability_incremental_analysis_members_hinge_forces(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def StabilityIncrementalAnalysisMembersInternalForces(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_stability_incremental_analysis_members_internal_forces(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def StabilityIncrementalAnalysisMembersInternalForcesByMemberSet(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member Set number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER_SET.name, object_no)

        results = model.clientModel.service.get_results_for_stability_incremental_analysis_members_internal_forces_by_member_set(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def StabilityIncrementalAnalysisMembersInternalForcesByCrossSection(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Section number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_CROSS_SECTION.name, object_no)

        results = model.clientModel.service.get_results_for_stability_incremental_analysis_members_internal_forces_by_section(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def StabilityIncrementalAnalysisMembersLocalDeformations(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_stability_incremental_analysis_members_local_deformations(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def StabilityIncrementalAnalysisMembersStrains(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_stability_incremental_analysis_members_strains(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def StabilityIncrementalAnalysisNodesDeformations(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Node number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_NODE.name, object_no)

        results = model.clientModel.service.get_results_for_stability_incremental_analysis_nodes_deformations(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def StabilityIncrementalAnalysisNodesSupportForces(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Node number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_NODE.name, object_no)

        results = model.clientModel.service.get_results_for_stability_incremental_analysis_nodes_support_forces(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def StabilityIncrementalAnalysisSummary(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Object number
            model (class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_stability_incremental_analysis_summary(loading_type.name, loading_no, object_no), include_base)


    @staticmethod
    def Summary(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Object number
            model (class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_summary(loading_type.name, loading_no))


    @staticmethod
    def TimeHistoryAnalysisBuildingStoriesCentresMassRigidity(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Object number
            model (class, optional): Model instance
        '''

        results = model.clientModel.service.get_results_for_time_history_analysis_building_stories_centres_mass_rigidity(
            loading_type.name,
            loading_no,
            object_locations = None # TODO: add filtering by Story number
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def TimeHistoryAnalysisBuildingStoriesForcesInShearWalls(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Object number
            model (class, optional): Model instance
        '''

        results = model.clientModel.service.get_results_for_time_history_analysis_building_stories_forces_in_shear_walls(
            loading_type.name,
            loading_no,
            object_locations = None # TODO: add filtering by Shear Wall number
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def TimeHistoryAnalysisBuildingStoriesInterstoryDrifts(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Object number
            model (class, optional): Model instance
        '''

        results = model.clientModel.service.get_results_for_time_history_analysis_building_stories_interstory_drifts(
            loading_type.name,
            loading_no,
            object_locations = None # TODO: add filtering by Story number
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def TimeHistoryAnalysisBuildingStoriesStoryActions(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Object number
            model (class, optional): Model instance
        '''

        results = model.clientModel.service.get_results_for_time_history_analysis_building_stories_story_actions(
            loading_type.name,
            loading_no,
            object_locations = None # TODO: add filtering by Story number
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def TimeHistoryAnalysisMembersContactForces(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_time_history_analysis_members_contact_forces(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def TimeHistoryAnalysisMembersGlobalDeformations(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_time_history_analysis_members_global_deformations(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def TimeHistoryAnalysisMembersHingeDeformations(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_time_history_analysis_members_hinge_deformations(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def TimeHistoryAnalysisMembersHingeForces(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_time_history_analysis_members_hinge_forces(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def TimeHistoryAnalysisMembersInternalForces(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_time_history_analysis_members_internal_forces(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def TimeHistoryAnalysisMembersInternalForcesByMemberSet(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member Set number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER_SET.name, object_no)

        results = model.clientModel.service.get_results_for_time_history_analysis_members_internal_forces_by_member_set(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def TimeHistoryAnalysisMembersInternalForcesByCrossSection(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Section number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_CROSS_SECTION.name, object_no)

        results = model.clientModel.service.get_results_for_time_history_analysis_members_internal_forces_by_section(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def TimeHistoryAnalysisMembersLocalDeformations(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_time_history_analysis_members_local_deformations(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def TimeHistoryAnalysisMembersStrains(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Member number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_MEMBER.name, object_no)

        results = model.clientModel.service.get_results_for_time_history_analysis_members_strains(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def TimeHistoryAnalysisNodesAccelerations(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Node number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_NODE.name, object_no)

        results = model.clientModel.service.get_results_for_time_history_analysis_nodes_accelerations(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def TimeHistoryAnalysisNodesDeformations(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Node number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_NODE.name, object_no)

        results = model.clientModel.service.get_results_for_time_history_analysis_nodes_deformations(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def TimeHistoryAnalysisNodesSupportForces(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Node number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_NODE.name, object_no)

        results = model.clientModel.service.get_results_for_time_history_analysis_nodes_support_forces(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def TimeHistoryAnalysisNodesVelocities(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Node number
            model (class, optional): Model instance
        '''

        object_locations = CreateObjectLocation(ObjectTypes.E_OBJECT_TYPE_NODE.name, object_no)

        results = model.clientModel.service.get_results_for_time_history_analysis_nodes_velocities(
            loading_type.name,
            loading_no,
            object_locations
        )

        return ConvertResultsToListOfDct(results, include_base)


    @staticmethod
    def TimeHistoryAnalysisSummary(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 1,
        object_no: int = 0,
        include_base: bool = False,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            object_no (int): Object number
            model (class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_time_history_analysis_summary(loading_type.name, loading_no, object_no), include_base)


    @staticmethod
    def HasAnyResults( model = Model):

        '''
         Args:
            model (class, optional): Model instance
        '''

        return model.clientModel.service.has_any_results()


    @staticmethod
    def HasResults(
        loading_type: enum = CaseObjectType.E_OBJECT_TYPE_LOAD_CASE,
        loading_no: int = 0,
        model = Model):

        '''
         Args:
            loading_type (enum): Loading type (LC2 = E_OBJECT_TYPE_LOAD_CASE)
            loading_no (int): Loading Number (CO2 = 2)
            model (class, optional): Model instance
        '''

        return model.clientModel.service.has_results(loading_type.name, loading_no)


    @staticmethod
    def AluminumDesignDesignRatiosMemberRepresentativesByConstructionStage(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_design_ratios_member_representatives_by_construction_stage(), include_base)


    @staticmethod
    def AluminumDesignDesignRatiosMemberRepresentativesByDesignSituation(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_design_ratios_member_representatives_by_design_situation(), include_base)


    @staticmethod
    def AluminumDesignDesignRatiosMemberRepresentativesByLoading(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_design_ratios_member_representatives_by_loading(), include_base)


    @staticmethod
    def AluminumDesignDesignRatiosMemberRepresentativesByLocation(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_design_ratios_member_representatives_by_location(), include_base)


    @staticmethod
    def AluminumDesignDesignRatiosMemberRepresentativesByMaterial(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_design_ratios_member_representatives_by_material(), include_base)


    @staticmethod
    def AluminumDesignDesignRatiosMemberRepresentativesByMemberRepresentative(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_design_ratios_member_representatives_by_member_representative(), include_base)


    @staticmethod
    def AluminumDesignDesignRatiosMemberRepresentativesByCrossSection(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_design_ratios_member_representatives_by_section(), include_base)


    @staticmethod
    def AluminumDesignDesignRatiosMemberSetRepresentativesByConstructionStage(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_design_ratios_member_set_representatives_by_construction_stage(), include_base)


    @staticmethod
    def AluminumDesignDesignRatiosMemberSetRepresentativesByDesignSituation(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_design_ratios_member_set_representatives_by_design_situation(), include_base)


    @staticmethod
    def AluminumDesignDesignRatiosMemberSetRepresentativesByLoading(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_design_ratios_member_set_representatives_by_loading(), include_base)


    @staticmethod
    def AluminumDesignDesignRatiosMemberSetRepresentativesByLocation(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_design_ratios_member_set_representatives_by_location(), include_base)


    @staticmethod
    def AluminumDesignDesignRatiosMemberSetRepresentativesByMaterial(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_design_ratios_member_set_representatives_by_material(), include_base)


    @staticmethod
    def AluminumDesignDesignRatiosMemberSetRepresentativesByMemberSetRepresentative(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_design_ratios_member_set_representatives_by_member_set_representative(), include_base)


    @staticmethod
    def AluminumDesignDesignRatiosMemberSetRepresentativesByCrossSection(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_design_ratios_member_set_representatives_by_section(), include_base)


    @staticmethod
    def AluminumDesignDesignRatiosMembersByConstructionStage(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_design_ratios_members_by_construction_stage(), include_base)


    @staticmethod
    def AluminumDesignDesignRatiosMembersByDesignSituation(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_design_ratios_members_by_design_situation(), include_base)


    @staticmethod
    def AluminumDesignDesignRatiosMembersByLoading(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_design_ratios_members_by_loading(), include_base)


    @staticmethod
    def AluminumDesignDesignRatiosMembersByLocation(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_design_ratios_members_by_location(), include_base)


    @staticmethod
    def AluminumDesignDesignRatiosMembersByMaterial(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_design_ratios_members_by_material(), include_base)


    @staticmethod
    def AluminumDesignDesignRatiosMembersByMember(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_design_ratios_members_by_member(), include_base)


    @staticmethod
    def AluminumDesignDesignRatiosMembersByMemberSet(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_design_ratios_members_by_member_set(), include_base)


    @staticmethod
    def AluminumDesignDesignRatiosMembersByCrossSection(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_design_ratios_members_by_section(), include_base)


    @staticmethod
    def AluminumDesignGoverningInternalForcesByMember(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_governing_internal_forces_by_member(), include_base)


    @staticmethod
    def AluminumDesignGoverningInternalForcesByMemberEnds(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_governing_internal_forces_by_member_ends(), include_base)


    @staticmethod
    def AluminumDesignGoverningInternalForcesByMemberRepresentative(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_governing_internal_forces_by_member_representative(), include_base)


    @staticmethod
    def AluminumDesignGoverningInternalForcesByMemberRepresentativeEnds(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_governing_internal_forces_by_member_representative_ends(), include_base)


    @staticmethod
    def AluminumDesignGoverningInternalForcesByMemberSet(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_governing_internal_forces_by_member_set(), include_base)


    @staticmethod
    def AluminumDesignGoverningInternalForcesByMemberSetEnds(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_governing_internal_forces_by_member_set_ends(), include_base)


    @staticmethod
    def AluminumDesignGoverningInternalForcesByMemberSetRepresentative(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_governing_internal_forces_by_member_set_representative(), include_base)


    @staticmethod
    def AluminumDesignGoverningInternalForcesByMemberSetRepresentativeEnds(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_governing_internal_forces_by_member_set_representative_ends(), include_base)


    @staticmethod
    def AluminumDesignGoverningLoading(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_governing_loading(), include_base)


    @staticmethod
    def AluminumDesignOverviewErrorsAndWarnings(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_overview_errors_and_warnings(), include_base)


    @staticmethod
    def AluminumDesignOverviewNotValidDeactivated(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_overview_not_valid_deactivated(), include_base)


    @staticmethod
    def AluminumDesignSlendernessByMember(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_slenderness_by_member(), include_base)


    @staticmethod
    def AluminumDesignSlendernessByMemberRepresentative(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_slenderness_by_member_representative(), include_base)


    @staticmethod
    def AluminumDesignSlendernessByMemberSet(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_slenderness_by_member_set(), include_base)


    @staticmethod
    def AluminumDesignSlendernessByMemberSetRepresentative(
        include_base: bool = False,
        model = Model):

        '''
        Args:
            model(class, optional): Model instance
        '''

        return ConvertResultsToListOfDct(model.clientModel.service.get_results_for_aluminum_design_slenderness_by_member_set_representative(), include_base)
