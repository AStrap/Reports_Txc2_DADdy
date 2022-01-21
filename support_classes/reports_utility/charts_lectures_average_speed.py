# -*- coding: utf-8 -*-
import math
import datetime

import config

class Charts_lectures_average_speed:

    PATH_OUTPUT = config.PATH_OUTPUT
    UNIT = config.TIME_UNIT 

    def __init__(self, dm, em):
        # data manager
        self.dm = dm

        # excel manager
        self.em = em

        return

    def compute_print(self, id_course):
        path_output_course = "%s\\%s-%s\\" %(self.PATH_OUTPUT, id_course, self.dm.get_course_name(id_course))

        workbook_name = "average_speed_%s.xlsx" %(self.dm.get_course_name(id_course))
        self.em.set_workbook(workbook_name, path_output_course)

        self.compute_support("Supporto_grafici", id_course)

        self.compute_average_speed("Velocita_di_visione", "Supporto_grafici", id_course)

        self.em.close_workbook()
        
        return workbook_name

    #-
    # Calcolo e produzione del foglio di supporto per studio dei vari punti di
    # interesse, in base a particolari criteri
    #-
    def compute_support(self, sheet, id_course):

        self.em.add_worksheet(sheet)

        for l in self.dm.get_lectures_by_course(id_course):

            #-- calcolo velocità medie per lezione
            info_speed = self.compute_speed(l, self.dm.get_sessions_by_course_lecture(id_course, l))
            #--

            #-- scrittura elementi
            head = [[str(datetime.timedelta(seconds=i*self.UNIT)) for i in range(math.ceil(self.dm.get_lecture_duration(l)/self.UNIT)+1)]]
            body = [[]]

            for i,s in enumerate(info_speed[1:]):
                tmp = ["" for _ in range(i)]
                tmp.append(s); tmp.append(s)
                body[0].extend(tmp)

            self.em.write_head_table(head)
            self.em.write_body_table(body)
            #--



        return

    #-
    # stampa i grafici delle medie di velocità
    #-
    def compute_average_speed(self, sheet, support_sheet, id_course):

        for i,l in enumerate(self.dm.get_lectures_by_course(id_course)):

            if i==0:
                self.em.add_worksheet_support_sheet("%s%d" %(sheet,i))
            else:
                self.em.add_worksheet("%s%d" %(sheet,i))

            if self.dm.get_lecture_duration(l)==0:
                self.em.print_line_chart("oriz", (i*2,(i*2)+1), (0, 0), support_sheet, "Velocità media - %s" %(self.dm.get_lecture_name(l)), "minutaggio", "livello di velocità", 1, 1, {'max':4, 'min':0, 'major_unit':1})
                continue

            x = [i*2, (i*2)+1]
            y = [0, math.ceil(self.dm.get_lecture_duration(l)/self.UNIT)]

            #- inserimento dei skip
            c_y=0
            # spazi bianchi
            s=0
            while s<math.ceil(self.dm.get_lecture_duration(l)/self.UNIT)-1:
                y_s = c_y; y_e = c_y+s+1
                y.append((y_s, y_e))

                c_y += s+2
                s += 1

            title = "Velocità media - %s" %(self.dm.get_lecture_name(l))
            self.em.print_line_chart_speed(x, y, support_sheet, title, "minutaggio", "livello di velocità", 1, 1, {"max":4, "min":0})


        return

    #-
    # elabera le medie di velocità
    #-
    def compute_speed(self, id_lecture, sessions):

        info_speed = [[] for _ in range(math.floor(self.dm.get_lecture_duration(id_lecture)/self.UNIT)+1)]

        for s in sessions:
            # sessioni che durano più di 1 minuto

            #tempo lezione e velocita lezione correnti
            t_cor = 0; v_cor = 1; play=0
            for e in s[3]:
                if int(e[2])>t_cor:
                    if play == 1:
                        #aggiornamento velocita intervalli tra t_cor e t rispetto al evento
                        while int(e[2])>=t_cor:
                            info_speed[math.floor(t_cor/self.UNIT)].append(v_cor)
                            t_cor += self.UNIT
                t_cor = int(e[2])

                if e[0] in ["S0", "S1", "S2", "S3", "S4"]:
                    v_cor = int(e[0][1])
                elif e[0]=="PL":
                    play = 1
                elif e[0]=="PS":
                    play = 0


        r_info_speed = [0 for _ in range(math.ceil(self.dm.get_lecture_duration(id_lecture)/self.UNIT)+1)]
        for i,inter in enumerate(info_speed):
            if len(inter)>0:
                #media velocità usata
                r_info_speed[i] = sum(inter)/len(inter)
            else:
                r_info_speed[i] = 0
        return r_info_speed