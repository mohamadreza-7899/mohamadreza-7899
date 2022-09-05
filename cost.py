from collect_data import CollectData


class Cost(CollectData):
    def longitudinal(self):

        self.etabs.Analyze.RunAnalysis()
        self.etabs.DesignConcrete.StartDesign()
        general_data = self.general_frame_data()
        frames = self.get_full_frame_data(general_frame_data=general_data)

        names = []
        for ID in frames:
            tidy = [ID]
            if tidy[:][0]['label'].startswith("B"):
                names.append(tidy[:][0]['id'])

        beam = []
        for ID in range(len(names)):
            beam.append(self.etabs.DesignConcrete.GetSummaryResultsBeam(names[ID]))
        return beam

    def get_location(self, general_data):
        name_id = self.get_beams_unique_names(general_frame_data=general_data)
        location = []
        for ID in name_id:
            location.append(self.etabs.DesignConcrete.GetSummaryResultsBeam(ID)[2])
        return location

    def solution(self, location):
        fin_location = []
        for loc in location.copy():
            result = []
            loc = [0] + list(loc)
            for idx in range(1, len(loc)):
                result.append(loc[idx] - loc[idx - 1])
            fin_location.append(result)
        return fin_location

    def get_top_area(self, general_data):
        name_id = self.get_beams_unique_names(general_frame_data=general_data)
        beam_top_area = []
        for ID in name_id:
            beam_top_area.append(self.etabs.DesignConcrete.GetSummaryResultsBeam(ID)[4])
        return beam_top_area

    def get_bot_area(self, general_data):
        name_id = self.get_beams_unique_names(general_frame_data=general_data)
        beam_bot_area = []
        for ID in name_id:
            beam_bot_area.append(self.etabs.DesignConcrete.GetSummaryResultsBeam(ID)[6])
        return beam_bot_area

    def get_tl_area(self, general_data):
        name_id = self.get_beams_unique_names(general_frame_data=general_data)
        beam_tl_area = []
        for ID in name_id:
            beam_tl_area.append(self.etabs.DesignConcrete.GetSummaryResultsBeam(ID)[10])
        return beam_tl_area

    def total_area(self, general_data):
        name_id = self.get_beams_unique_names(general_frame_data=general_data)
        total_area = []
        top = self.get_top_area(general_data)
        bot = self.get_bot_area(general_data)
        tl = self.get_tl_area(general_data)
        for ID in range(len(name_id)):
            for column in range(len(top[ID])):
                total_area.append(top[ID][column] + bot[ID][column] + tl[ID][column])
        return total_area

    def volume_longitudinal_beam(self, general_data, location):
        name_id = self.get_beams_unique_names(general_frame_data=general_data)
        volume_beam = []
        length = self.solution(location)
        area = self.total_area(general_data)
        index_area = 0
        for ID in range(len(name_id)):
            summation = 0
            for j in range(len(length[ID])):
                summation += length[ID][j]*area[index_area]
                index_area += 1
            volume_beam.append(summation)
        return sum(volume_beam)

    def major_area(self, general_data):
        name_id = self.get_beams_unique_names(general_frame_data=general_data)
        major_area_list = []
        for ID in name_id:
            major_area_list.append(self.etabs.DesignConcrete.GetSummaryResultsBeam(ID)[8])
        return major_area_list

    def tt_area(self, general_data):
        name_id = self.get_beams_unique_names(general_frame_data=general_data)
        tt_area_list = []
        for ID in name_id:
            tt_area_list.append(self.etabs.DesignConcrete.GetSummaryResultsBeam(ID)[12])
        return tt_area_list

    def trans_beam_area(self, general_data):
        name_id = self.get_beams_unique_names(general_frame_data=general_data)
        trans_area = []
        major = self.major_area(general_data)
        tt = self.tt_area(general_data)
        for ID in range(len(name_id)):
            for column in range(len(major[ID])):
                trans_area.append(major[ID][column] + 2*tt[ID][column])
        return trans_area

    def section_full(self, general_data):
        name_id = self.get_full_frame_data(general_frame_data=general_data)
        return name_id

    def section_width(self, general_data):
        name_id = self.get_full_frame_data(general_frame_data=general_data)
        names = []
        for ID in name_id:
            tidy = [ID]
            if tidy[:][0]['label'].startswith("B"):
                names.append(tidy[:][0]['width'])
        return names

    def section_height(self, general_data):
        name_id = self.get_full_frame_data(general_frame_data=general_data)
        names = []
        for ID in name_id:
            tidy = [ID]
            if tidy[:][0]['label'].startswith("B"):
                names.append(tidy[:][0]['height'])
        return names

    def section_length(self, general_data):
        name_id = self.get_full_frame_data(general_frame_data=general_data)
        names = []
        for ID in name_id:
            tidy = [ID]
            if tidy[:][0]['label'].startswith("B"):
                names.append(tidy[:][0]['length'])
        return names

    def stirrup_length(self, general_data):
        perimeter = []
        width = self.section_width(general_data)
        height = self.section_height(general_data)
        for ID in range(len(width)):
            perimeter.append(2*((width[ID]-8) + (height[ID]-8)))
        return perimeter

    def volume_trans_beam(self, general_data):
        volume_beam = []
        length = self.section_length(general_data)
        stirrup = self.stirrup_length(general_data)
        area = self.trans_beam_area(general_data)
        for ID in range(len(length)):
            volume_beam.append(length[ID] * area[ID] * stirrup[ID])
        return sum(volume_beam)

    def location_column(self, general_data):
        name_id = self.get_columns_unique_names(general_frame_data=general_data)
        location_list = []
        for ID in name_id:
            location_list.append(self.etabs.DesignConcrete.GetSummaryResultsColumn(ID)[3][2])
        return location_list

    def area_column(self, general_data):
        name_id = self.get_columns_unique_names(general_frame_data=general_data)
        long_column_list = []
        for ID in name_id:
            long_column_list.append(self.etabs.DesignConcrete.GetSummaryResultsColumn(ID)[5][2])
        return long_column_list

    def volume_longitudinal_column(self, general_data):
        volume_column = []
        location = self.location_column(general_data)
        area = self.area_column(general_data)
        for ID in range(len(location)):
            volume_column.append(location[ID] * area[ID])
        return sum(volume_column)

    def major_column(self, general_data):
        name_id = self.get_columns_unique_names(general_frame_data=general_data)
        major_column_list = []
        for ID in name_id:
            major_column_list.append(self.etabs.DesignConcrete.GetSummaryResultsColumn(ID)[8])
        return major_column_list

    def minor_column(self, general_data):
        name_id = self.get_columns_unique_names(general_frame_data=general_data)
        minor_column_list = []
        for ID in name_id:
            minor_column_list.append(self.etabs.DesignConcrete.GetSummaryResultsColumn(ID)[10])
        return minor_column_list

    def max_minor_major(self, general_data):
        maximum = []
        minor = self.minor_column(general_data)
        major = self.major_column(general_data)
        for ID in range(len(minor)):
            maximum.append(max(minor[ID], major[ID])[0])
        return maximum

    def column_width(self, general_data):
        name_id = self.get_full_frame_data(general_frame_data=general_data)
        names = []
        for ID in name_id:
            tidy = [ID]
            if tidy[:][0]['label'].startswith("C"):
                names.append(tidy[:][0]['width'])
        return names

    def column_height(self, general_data):
        name_id = self.get_full_frame_data(general_frame_data=general_data)
        names = []
        for ID in name_id:
            tidy = [ID]
            if tidy[:][0]['label'].startswith("C"):
                names.append(tidy[:][0]['height'])
        return names

    def column_length(self, general_data):
        name_id = self.get_full_frame_data(general_frame_data=general_data)
        names = []
        for ID in name_id:
            tidy = [ID]
            if tidy[:][0]['label'].startswith("C"):
                names.append(tidy[:][0]['length'])
        return names

    def stirrup_length_column(self, general_data):
        perimeter = []
        width = self.column_width(general_data)
        height = self.column_height(general_data)
        for ID in range(len(width)):
            perimeter.append(2*((width[ID]-8) + (height[ID]-8)))
        return perimeter

    def volume_trans_column(self, general_data):
        volume_column = []
        length = self.column_length(general_data)
        stirrup = self.stirrup_length_column(general_data)
        area = self.max_minor_major(general_data)
        for ID in range(len(length)):
            volume_column.append(length[ID] * area[ID] * stirrup[ID])
        return sum(volume_column)

    def total_volume_rebar(self, general_data, location):
        beam_long = self.volume_longitudinal_beam(general_data, location)
        beam_trans = self.volume_trans_beam(general_data)
        column_long = self.volume_longitudinal_column(general_data)
        column_trans = self.volume_trans_column(general_data)
        total_volume = beam_long + beam_trans + column_trans + column_long
        return total_volume

    def total_mass(self, general_data, location):
        constant_value = 7850
        total = self.total_volume_rebar(general_data, location)
        total_mass = constant_value*total
        return total_mass

    def total_value(self, general_data, location):
        constants_value = 155500
        total_value = self.total_mass(general_data, location)
        final_value = constants_value*total_value
        return final_value


class FrameWorkCost(CollectData):

    def framework_beam_width(self, total_data):
        name_id = self.get_full_frame_data(general_frame_data=total_data)
        names = []
        for ID in name_id:
            tidy = [ID]
            if tidy[:][0]['label'].startswith("B"):
                names.append(tidy[:][0]['width'])
        return names

    def framework_beam_height(self, total_data):
        name_id = self.get_full_frame_data(general_frame_data=total_data)
        names = []
        for ID in name_id:
            tidy = [ID]
            if tidy[:][0]['label'].startswith("B"):
                names.append(tidy[:][0]['height'])
        return names

    def framework_column_width(self, total_data):
        name_id = self.get_full_frame_data(general_frame_data=total_data)
        names = []
        for ID in name_id:
            tidy = [ID]
            if tidy[:][0]['label'].startswith("C"):
                names.append(tidy[:][0]['width'])
        return names

    def framework_column_height(self, total_data):
        name_id = self.get_full_frame_data(general_frame_data=total_data)
        names = []
        for ID in name_id:
            tidy = [ID]
            if tidy[:][0]['label'].startswith("C"):
                names.append(tidy[:][0]['height'])
        return names

    def framework_column_length(self, total_data):
        name_id = self.get_full_frame_data(general_frame_data=total_data)
        names = []
        for ID in name_id:
            tidy = [ID]
            if tidy[:][0]['label'].startswith("C"):
                names.append(tidy[:][0]['length'])
        return names

    def framework_beam_length(self, total_data):
        name_id = self.get_full_frame_data(general_frame_data=total_data)
        names = []
        for ID in name_id:
            tidy = [ID]
            if tidy[:][0]['label'].startswith("B"):
                names.append(tidy[:][0]['length'])
        return names

    def beam_frame_cost(self, total_data):
        beam_cost = []
        width = self.framework_beam_width(total_data)
        height = self.framework_beam_height(total_data)
        length = self.framework_beam_length(total_data)
        for ID in range(len(width)):
            beam_cost.append((2*height[ID] + width[ID])*length[ID])
        return sum(beam_cost)

    def column_frame_cost(self, total_data):
        column_cost = []
        width = self.framework_column_width(total_data)
        height = self.framework_column_height(total_data)
        length = self.framework_column_length(total_data)
        for ID in range(len(width)):
            column_cost.append((2*(height[ID] + width[ID]))*length[ID])
        return sum(column_cost)

    def total_frame_cost(self, total_data):
        beam = self.beam_frame_cost(total_data)
        column = self.column_frame_cost(total_data)
        total = beam + column
        return total

    def total_value(self, total_data):
        constants_value = 1038000
        total_value = self.total_frame_cost(total_data)
        final_value = constants_value*total_value
        return final_value
