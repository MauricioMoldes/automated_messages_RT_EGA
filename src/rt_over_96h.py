#!/usr/bin/env python

""" rt_over_96H.py: Replies to HelpDesk Request Tracker tickets over 96H with static message"""

__author__ = "Mauricio Moldes"
__version__ = "0.1"
__maintainer__ = "Mauricio Moldes"
__email__ = "mauricio.moldes@crg.eu"
__status__ = "Developement"

import logging
import sys
import yaml
import rt

logger = logging.getLogger('rt_over_96H')

""" LOGIN RT """


def login_rt_request(cfg):
    tracker = rt.Rt(str(cfg['request_tracker_db']['address']), str(cfg['request_tracker_db']['user']),
                    str(cfg['request_tracker_db']['password']))
    tracker.login()
    return tracker


""" READ CONFIG FILE """


def read_config(path):
    with open(path, 'r') as stream:
        results = yaml.safe_load(stream)
    return results


""" GETS LIST OF TARGET TICKETS, REPLIES AND UPDATE TICKET STATUS """


def get_target_tickets(conn_tracker):
    tickets = conn_tracker.search(Queue='sanger.ac.uk: ebi-ega-helpdesk', Status='new', LastUpdated__lt='-2 day')
    for ticket in tickets:
        id = ticket['id'][7:]  # get ticket id
        logger.info("RT: " + str(id) + " updated")  # info
        print("ID:" + id)  # print ticket ID to console
        reply(conn_tracker, id)  # replies to ticket with static message
        change_status(conn_tracker, id)  # changes ticket status to new
    return tickets


""" UPDATES TICKET STATUS TO NEW """


def change_status(conn_tracker, id):
    conn_tracker.edit_ticket(id, Status='new', Owner='Nobody')


""" REPLIES TO RT RICKET WITH STATIC MESSAGE """


def reply(conn_tracker, id):
    static_reply_message = """ Thank you for your patience. Please be assured that your ticket will be dealt with as soon as possible. In the meantime, please kindly refrain from creating multiple tickets for the same issue.
    
    Kind regards,
    EGA Team """
    conn_tracker.reply(id, text=static_reply_message)


""" VERIFIES CONNECTION TO DB's  """


def reply_96h_new_tickets(cfg):
    conn_tracker = None
    try:
        conn_tracker = login_rt_request(cfg)  # conn to request Tracker
        if conn_tracker:  # has required connections
            tickets = get_target_tickets(conn_tracker)
            if not tickets:
                logger.info("No tickets over 96H")  # info
                print("No tickets over 96H")  # print to console
        else:
            logger.debug("RT is not available")
            logger.info("RT over 96H process ended")
    except Exception as e:
        logger.error("Error: {}".format(e))
    finally:
        if conn_tracker:
            conn_tracker.logout()
            logger.debug("Request Tracker connection closed")


""" MAIN """


def run():
    try:
        # configure logging
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s [in %(pathname)s:%(lineno)d]'
        logging.basicConfig(format=log_format)
        # read config file
        cfg = read_config("../bin/config.yml")
        # execute main function
        reply_96h_new_tickets(cfg)
    except Exception as e:
        logger.error("Error: {}".format(e))
        sys.exit(-1)


if __name__ == '__main__':
    ## cue the music
    run()
