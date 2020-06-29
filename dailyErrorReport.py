#!/usr/bin/env python3

import os
import subprocess


def getPrefix():
    cmd = "psql -c 'show log_line_prefix;'"

    processPrefix = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outPrefix, errPrefix = processPrefix.communicate()
    return outPrefix.splitlines()[2].decode()[1:-1]


def getHostName():
    cmd = "hostname"

    processHostname = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outHostname, errHostname = processHostname.communicate()
    return outHostname.splitlines()[0].decode()


def getLogDir():
    cmd = "pg_lsclusters"

    processLogDir = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outLogDir, errLogDir = processLogDir.communicate()
    listLogDir = list(outLogDir.splitlines()[1].decode().split())
    return listLogDir[-2] + "/" + listLogDir[-1].split("/")[0] + "/"


def getLastLogFile(logfile):
    cmd = "ls -t " + logfile

    processLogFile = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outlogfile, errlogfile = processLogFile.communicate()
    return list(outlogfile.split())[0].decode()


def getDate():
    cmd = "date +\\%F"

    processToday = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outToday, errToday = processToday.communicate()
    return outToday[:-1].decode()


def getParameter():
    parameters = ["w", "q"]     # these parameter for only error in quiet mode (don't print anything to stdout)
    return " ".join(map(lambda x: " -" + x, parameters))


def executePgbadger(prefix,parameter, hostname, logdir, errordir, logfile, today):
    cmd = "/usr/bin/pgbadger --prefix '" + prefix + "' "+ parameter +" --outfile " + errordir + "/pgbadger-" + today + "-" + hostname + "-Errors.html " + logdir + logfile

    processLogDir = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outLogDir, errLogDir = processLogDir.communicate()


def main():
    pgbadgerErrorFolder = 'pgbadgerError'

    try:
        os.mkdir(pgbadgerErrorFolder)
    except OSError:
        pass
    finally:
        logPrefix = getPrefix()
        hostName = getHostName()
        logDirectory = getLogDir()
        lastLogFile = getLastLogFile(logDirectory)
        todayDate = getDate()
        parameter = getParameter()
        executePgbadger(logPrefix, parameter, hostName, logDirectory, pgbadgerErrorFolder, lastLogFile, todayDate)


if __name__ == "__main__":
    main()

