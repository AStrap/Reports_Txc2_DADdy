# -*- coding: utf-8 -*-
import config
import utility.time_date as time_date

class Chart_user_agents:

    PATH_OUTPUT = config.PATH_OUTPUT
    DAY_PERIODS = config.DAY_PERIODS
    USER_AGENTS = config.USER_AGENTS

    def __init__(self, dm):
        # data manager
        self.dm = dm

        return

    """
        Calcolo e stampa grafici riguardo l'uso dei dispositivi

        Parametri:
            - id_course: str
                corso di riferimento

        Return:
            - workbook_name: str
                nome file excel in cui salvati i grafici
    """
    def compute_print(self, id_course):
        path_output_course = "%s\\%s-%s\\" %(self.PATH_OUTPUT, id_course, self.dm.get_course_name(id_course))

        workbook_name = "user_agents_%s.xlsx" %(self.dm.get_course_name(id_course))
        self.em.set_workbook(workbook_name, path_output_course)

        self.print_charts_user_agents("User_agents", id_course)

        self.em.close_workbook()

        return workbook_name

    """
        Stampa grafici dispositivi

        Parametri:
            - sheet: str
                nome foglio su cui stampare i grafici

            - id_course: str
                corso di riferimento

    """
    def print_charts_user_agents(self, sheet, id_course):

        self.em.add_worksheet("%s" %(sheet))
        self.em.set_cursors(1,1)

        user_agents = self.compute_user_agents(id_course)

        head = [[""]]
        user_agents_series = list()
        for ua in self.USER_AGENTS:
            head[0].append(ua[0])
            user_agents_series.append(ua[0])
        self.em.write_head_table(head)

        body = [[] for _ in range(len(self.DAY_PERIODS)) ]
        for i,d in enumerate(self.DAY_PERIODS):
            body[i].append("[%s:%s)" %(d[0], d[1]))
        for user_agent in user_agents:
            for i,n_in_period in enumerate(user_agent):
                body[i].append(n_in_period)
        self.em.write_body_table(body)

        x = (2, 1+len(self.DAY_PERIODS)); y = [i+1 for i in range(len(self.USER_AGENTS)+1)]
        title = "Numero dispositivi usati durante la giornata"
        self.em.print_column_chart_multp("vert", x, y, user_agents_series, sheet, title, "periodo giornata", "numero dispositivi", 2+len(self.USER_AGENTS), 1, {'min':0})

        return

    """
        Calcolo distribuzione dei dispositivi usati dagli utenti

        Parametri:
            - id_course: str
                corso di riferimento

        Retunr:
            - user_agents: list() (es. [[1,2,3,4],[1,2,3,4]])
                numero dispositivi per tipo e per periodo di giornata
    """
    def compute_user_agents(self, id_course):
        user_agents = [[0 for _ in range(len(self.DAY_PERIODS))] for _ in range(len(self.USER_AGENTS))]

        sessions = self.dm.get_sessions_by_course(id_course)

        for s in sessions:

            user_agent = s[2]
            timestamp = s[1]

            #-- calcolo user_agent
            ind_user_agent = len(self.USER_AGENTS) - 1
            i = 0
            for ua in self.USER_AGENTS[:-1]:
                for device in ua[1]:
                    if device in user_agent:
                        ind_user_agent = i
                if ind_user_agent == i:
                    break
                i += 1
            #--


            #-- calcolo periodo giornata
            day = timestamp[:10]
            timestamp = timestamp[:19]

            ind_period = 0
            i=0
            for day_period in self.DAY_PERIODS:
                first = "%sT%s" %(day, day_period[0])
                last = "%sT%s" %(day, day_period[1])
                if time_date.cmp_dates(timestamp, first)>=0 and time_date.cmp_dates(timestamp, last)<0:
                    ind_period = i
                i += 1
            #--

            user_agents[ind_user_agent][ind_period] += 1


        return user_agents
