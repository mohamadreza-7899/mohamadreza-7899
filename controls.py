import pandas as pd
from runetabs import RunConcrete


class Controls(RunConcrete):

    def torsional_irregularity(self):
        # Required Load Cases are : EX & EXP & EXN & EY & EYP & EYN
        self.etabs.DatabaseTables.SetLoadCasesSelectedForDisplay(['EX'])
        # getting all data for torsional_irregularity control
        torsion = self.etabs.DatabaseTables.GetTableForDisplayArray('Story Max Over Avg Drifts', [], '', 0, [], 0, [])
        # we just need titr and data to control torsional_irregularity ,so we get their indexes
        titr = torsion[2]
        data = torsion[4]
        lines = [list(titr)]
        j = 0
        # list of titr has 7 indexes so by using these indexes we separate all specific data and change them in one list
        for i in range(len(titr), len(data) + len(titr), len(titr)):
            lines.append(list(data[j:i]))
            j += len(titr)

        # in controlling torsional_irregularity we don't need to "CaseType" so we remove titr and total data of it.
        casetype_index = lines[0].index('CaseType')
        for i in range(len(lines)):
            lines[i].remove(lines[i][casetype_index])
        steptype_index = lines[0].index('StepType')
        for i in range(len(lines)):
            lines[i].remove(lines[i][steptype_index])

        vs_pos = []
        vs = []
        # we know for torsional_irregularity control ratio must be lower than 1.2 .so we added a titr as situation to
        # tell us is it ok or not.
        lines[0].append('Situation')
        all_not_ok_ratios = []
        for i in range(1, len(lines)):
            vs_pos.append(abs(float(lines[i][4])))
            vs_pos.append(abs(float(lines[i][5])))
            vs.append(float(lines[i][4]))
            vs.append(float(lines[i][5]))
            ratio = float(lines[i][lines[0].index('Ratio')])
            if ratio < 1.2:
                lines[i].append('OK')
            else:
                lines[i].append('Not OK')
                all_not_ok_ratios.append(ratio - 1.2)

        # type of data are string ,so we must change them to float
        for i in range(1, len(lines)):
            lines[i][-2] = float(lines[i][-2])
            lines[i][-3] = float(lines[i][-3])
            lines[i][-4] = float(lines[i][-4])

        df = pd.DataFrame(lines[1:], columns=lines[0])
        return df, sum(all_not_ok_ratios)

    def stiff_controls(self):
        self.etabs.DatabaseTables.SetLoadCasesSelectedForDisplay(['EX'])
        stiff = self.etabs.DatabaseTables.GetTableForDisplayArray('Story Stiffness', [], '', 0, [], 0, [])
        titr = stiff[2]
        data = stiff[4]

        lines = [list(titr)]
        j = 0
        for i in range(len(titr), len(data) + len(titr), len(titr)):
            lines.append(list(data[j:i]))
            j += len(titr)

        ShearX_index = lines[0].index('ShearX')
        DriftX_index = lines[0].index('DriftX')
        ShearY_index = lines[0].index('ShearY')
        DriftY_index = lines[0].index('DriftY')

        for i in range(len(lines)):
            lines[i].remove(lines[i][ShearX_index])
            lines[i].remove(lines[i][DriftX_index - 1])
            lines[i].remove(lines[i][ShearY_index - 2])
            lines[i].remove(lines[i][DriftY_index - 3])

        steptype_index = lines[0].index('StepType')
        for i in range(len(lines)):
            lines[i].remove(lines[i][steptype_index])
        vs_pos = []
        vs = []
        for i in range(1, len(lines)):
            vs_pos.append(abs(float(lines[i][-2])))
            vs_pos.append(abs(float(lines[i][-1])))
            vs.append(float(lines[i][-2]))
            vs.append(float(lines[i][-1]))

        df = pd.DataFrame(lines[1:], columns=lines[0])
        return df

    def rho_control(self):
        self.etabs.DatabaseTables.SetLoadCasesSelectedForDisplay(['EY'])
        rho = self.etabs.DatabaseTables.GetTableForDisplayArray('Story Forces', [], '', 0, [], 0, [])

        titr = rho[2]
        data = rho[4]

        lines = [list(titr)]
        j = 0
        for i in range(len(titr), len(data) + len(titr), len(titr)):
            lines.append(list(data[j:i]))
            j += len(titr)

        p_index = lines[0].index('P')
        t_index = lines[0].index('T')
        mx_index = lines[0].index('MX')
        my_index = lines[0].index('MY')
        casetype_index = lines[0].index('CaseType')

        for i in range(len(lines)):
            lines[i].remove(lines[i][casetype_index])
            lines[i].remove(lines[i][p_index - 1])
            lines[i].remove(lines[i][t_index - 2])
            lines[i].remove(lines[i][mx_index - 3])
            lines[i].remove(lines[i][my_index - 4])

        steptype_index = lines[0].index('StepType')
        for i in range(len(lines)):
            lines[i].remove(lines[i][steptype_index])

        lines[0].append('0.35*Vmax')
        vs_pos = []
        vs = []
        for i in range(1, len(lines)):
            vs_pos.append(abs(float(lines[i][-2])))
            vs_pos.append(abs(float(lines[i][-1])))
            vs.append(float(lines[i][-2]))
            vs.append(float(lines[i][-1]))

        v_max = max(vs_pos)
        v_max = vs[vs_pos.index(v_max)]
        for i in range(1, len(lines)):
            lines[i].append(str(0.35 * v_max))

        for i in range(1, len(lines)):
            lines[i][-3] = float(lines[i][-3])
            lines[i][-2] = float(lines[i][-2])
            lines[i][-1] = float(lines[i][-1])

        lines[0].append('Situation')
        for i in range(1, len(lines)):
            vx = abs(lines[i][lines[0].index('VX')])
            vy = abs(lines[i][lines[0].index('VY')])
            vmax = abs(lines[i][lines[0].index('0.35*Vmax')])
            if vmax < vx or vmax < vy:
                lines[i].append('OK')
            else:
                lines[i].append('Not OK')

        for i in range(1, len(lines)):
            lines[i][-4] = float(lines[i][-4])
            lines[i][-3] = float(lines[i][-3])
            lines[i][-2] = float(lines[i][-2])

        df = pd.DataFrame(lines[1:], columns=lines[0])
        df = df.loc[df.Location == 'Bottom']
        df.index = range(1, len(df.index) + 1)
        return df

    def check_stiff(self,df, n_story):
        x = df.to_dict("records")
        n_story = 4
        k = {
            "StiffX": [],
            "StiffY": [],
            "nim": []
        }
        u = 0
        while (u + 3) != len(x) - 1:
            c = 0
            while c != n_story:
                if c <= 3 and c + 1 <= 3 and c + 2 <= 3 and c + 3 <= 3:
                    mian_x = (x[u]['StiffX'] + x[u + 1]['StiffX'] + x[u + 2]['StiffX']) / 3
                    mian_y = (x[u]['StiffY'] + x[u + 1]['StiffY'] + x[u + 2]['StiffY']) / 3
                    try:
                        k["StiffX"].append(x[u + 3]['StiffX'] / mian_x)
                        k["StiffY"].append(x[u + 3]['StiffY'] / mian_y)
                    except ZeroDivisionError:
                        k["nim"].append(0)
                c = c + 1
                u = u + 1
        return k

