# -*- coding: utf-8 -*-
import os

import config
import utility.time_date as time_date

import support_classes.reports_utility.info_users as info_users
import support_classes.reports_utility.info_lectures as info_lectures
import support_classes.reports_utility.chart_lectures_events as chart_lectures_events
import support_classes.reports_utility.charts_sessions_days_distribution as charts_sessions_days_distribution
import support_classes.reports_utility.chart_sessions_hours_distribution as chart_sessions_hours_distribution
import support_classes.reports_utility.chart_course_vision as chart_course_vision
import support_classes.reports_utility.charts_lectures_average_speed as charts_lectures_average_speed
import support_classes.reports_utility.charts_lectures_vision as charts_lectures_vision
import support_classes.reports_utility.charts_lectures_seek_events as charts_lectures_seek_events

class Reports_manager:

    PATH_OUTPUT = config.PATH_OUTPUT
    DATE_RANGE_STUDY = config.DATE_RANGE_STUDY

    def __init__(self, dm):

        #-- data_manager
        self.dm = dm
        #--

        return

    """
        Return data del primo video pubblicato e dell'ultimo video pubblicato

        Parametri:
            - id_course: str
                corso di riferimento

        Return:
            - first_date: str (es. "YYYY-MM-DD")
                data primo video pubblicato

            - last_date: str (es. "YYYY-MM-DD")
                data ultimo video pubblicato
    """
    def get_first_last_lecture_dates(self, id_course):
        lectures = self.dm.get_lectures_by_course(id_course)

        first_date = self.dm.get_lecture_release_date(lectures[0])[:10]
        last_date = self.dm.get_lecture_release_date(lectures[-1])[:10]

        return first_date, last_date

    """
        Return data del primo appello d'esame e del secondo appello d'esame

        Parametri:
            - id_course: str
                corso di riferimento

            - exam_dates[0]: str (es. YYYY-MM-DD)
                data primo appello

            - exam_dates[1]: str (es. YYYY-MM-DD)
                data secondo appello
    """
    def get_first_second_exam_dates(self, id_course):
        exam_dates = self.dm.get_exam_dates(id_course)

        return exam_dates[0], exam_dates[1]

    """
        Return informazioni generali riguardo le lezioni

        Parametri:
            - id_course: str
                corso di riferimento

        Return:
            - info lezioni: list()
                lista informazioni di ogni lezione
    """
    def get_lectures_total_info(self, id_course):

        c_lectures = info_lectures.Info_lectures(self.dm)

        return c_lectures.compute_info_lectures(id_course)

    """
        Return intervalli di tempo dei due periodi

        Parametri:
            - id_course: str
                corso di riferimento

        Return:
            - first_period: (str, str)
                date di range del primo periodo

            - second_period: (str, str)
                date di range del secondo periodo
    """
    def get_periods(self, id_course):

        first_period = list(); second_period = list()

        first_lecture_date, last_lecture_date = self.get_first_last_lecture_dates(id_course)
        first_period.append(first_lecture_date)
        first_period.append(time_date.add_days(last_lecture_date, 2))

        tmp = time_date.get_datetime(time_date.add_days(last_lecture_date, 3))
        if tmp > time_date.get_datetime(self.DATE_RANGE_STUDY[1]):
            second_period=[str(tmp)[:10], "-"]
        else:
            second_period.append(str(tmp)[:10])
            second_period.append(self.DATE_RANGE_STUDY[1])

        return first_period, second_period

    """
        Return utenti dato id_corso e periodo di tempo

        Parametri:
            - period: (str, str)
                periodo di studio

            - id_course: str
                corso di riferimento

        Return:
            - users: list()
                lista utenti con almeno una sessione nel periodo
    """
    def users_period(self, period, id_course):

        days = time_date.get_days_by_period(period)

        users = list()

        for s in self.dm.get_sessions_by_course_days(id_course, days):
            if not s[-1] in users:
                users.append(s[-1])

        return users

    """
        Return sessioni dato id_corso e periodo di tempo

        Parametri:
            - period: (str, str)
                periodo di studio

            - id_course: str
                corso di riferimento

        Return:
            - info sessioni: list()
                lista informazioni di ogni sessione
    """
    def sessions_period(self, period, id_course):

        days = time_date.get_days_by_period(period)

        return self.dm.get_sessions_by_course_days(id_course, days)

    """
        Return informazioni riguardo un utente ed un corso specifico

        Parametri:
            - id_course: str
                corso di riferimento

        Return:
            - informazioni sugli utenti: list()
    """
    def get_users_info(self, id_course):
        c_users = info_users.Info_users(self.dm)

        return c_users.compute_info_users(id_course)

    """
        Return informazioni riguardo ai gruppi di utenti per corso specifico

        Parametri:
            - id_course: str
                corso di riferimento

        Return:
            - lista utenti per ogni cluster
    """
    def get_users_clusters(self, id_course):
        c_users = info_users.Info_users(self.dm)

        return c_users.compute_clusters_activity(id_course)

    """
        Return informazioni riguardo le keywords cercate

        Parametri:
            - id_course: str
                corso di riferimento

            - keywords: list()
                informazioni riguardo le keywords
    """
    def get_keywords(self, id_course):

        keywords = list()
        for id_lecture in self.dm.get_lectures_by_course(id_course):
            tmp = list()
            for s in self.dm.get_sessions_by_course_lecture(id_course, id_lecture):
                for e in s[3]:
                    if e[0]=="KW":
                        keyword = e[3]
                        timestamp = time_date.seconds_hours(e[2])
                        tmp.append([keyword, self.dm.get_lecture_name(id_lecture), timestamp, s[-1]])
            tmp.sort(key=lambda x:x[2])
            keywords.extend(tmp)

        return keywords

    #- GRAFICI ----------------------------------------------------------------
    """
        Stampa i grafici riguardo le sessioni distribuite per giorni e dalla
        data di pubblicazione di una lezione

        Parametri:
            - id_course: str
                corso di riferimento

            - periodo: (str, str)
                periodo di studio

            - label_periodo: str
                label come riferimento al periodo
    """
    def print_session_day_distribution(self, id_course, period, label_period):
        c_sessions_day_distribution = charts_sessions_days_distribution.Charts_sessions_days_distribution(self.dm)
        c_sessions_day_distribution.compute_print(id_course, label_period, period)

        return

    """
        Stampa i grafici riguardo le sessioni distribuite per giorni e dalla
        data di pubblicazione di una lezione

        Parametri:
            - id_course: str
                corso di riferimento

            - periodo: (str, str)
                periodo di studio

            - label_periodo: str
                label come riferimento al periodo
    """
    def print_session_hours_distribution(self, id_course, period, label_period):

        c_sessions_hours_distribution = chart_sessions_hours_distribution.Chart_sessions_hours_distribution(self.dm)
        c_sessions_hours_distribution.compute_print(id_course, label_period, period)

        return

    """
        Stampa grafico che indica la copertura di visione del corso: numero
        utenti per lezione

        Parametri:
            - id_course: str
                corso di riferimento

            - periodo: (str, str)
                periodo di studio

            - label_periodo: str
                label come riferimento al periodo
    """
    def print_course_vision(self, id_course, period, label_period):

        c_course_vision = chart_course_vision.Chart_course_vision(self.dm)
        c_course_vision.compute_print(id_course, label_period, period)

        return

    """
        Stampa i grafici riguardo il numero di eventi per lezione

        Parametri:
            - id_course: str
                corso di riferimento

            - periodo: (str, str)
                periodo di studio

            - label_periodo: str
                label come riferimento al periodo
    """
    def print_lectures_events(self, id_course, period, label_period):

        c_lectures_events = chart_lectures_events.Chart_lectures_events(self.dm)
        c_lectures_events.compute_print(id_course, label_period, period)
        return

    """
        Stampa grafico riguardo la copertura di visione della lezione

        Parametri:
            - id_course: str
                corso di riferimento
    """
    def print_lectures_vision(self, id_course):

        c_charts_lectures_vision = charts_lectures_vision.Charts_lectures_vision(self.dm)
        c_charts_lectures_vision.compute_print(id_course)

        return

    """
        Stampa grafico riguardo alla velocit?? media di visione di una lezione

        Parametri:
            - id_course: str
                corso di riferimento
    """
    def print_lectures_average_speed(self, id_course):

        c_charts_lectures_average_speed = charts_lectures_average_speed.Charts_lectures_average_speed(self.dm)
        c_charts_lectures_average_speed.compute_print(id_course)

        return

    """
        Stampa grafico riguardo la tipologia e il numero di eventi che puntano ad un specifico minutaggio

        Parametri:
            - id_course: str
                corso di riferimento
    """
    def print_lectures_seek_events(self, id_course):

        c_charts_lectures_seek_events = charts_lectures_seek_events.Charts_lectures_seek_events(self.dm)
        c_charts_lectures_seek_events.compute_print(id_course)

        return

    """
        Stampa grafico riguardo i dispositivi usati

        Parametri:
            - id_course: str
                corso di riferimento
    """
    def print_user_agent_info(self, id_course):

        c_chart_user_agents = chart_user_agents.Chart_user_agents(self.dm)
        c_chart_user_agents.compute_print(id_course)

        return
