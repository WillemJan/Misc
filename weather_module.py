#!/usr/bin/env python

import pymetar
import sys



def get_weather(station_name="EHAM"):
    station = station_name

    try:
        rf=pymetar.ReportFetcher(station)
        rep=rf.FetchReport()
    except Exception, e:
        sys.stderr.write("Something went wrong when fetching the report.\n")
        sys.stderr.write("These usually are transient problems if the station ")
        sys.stderr.write("ID is valid. \nThe error encountered was:\n")
        sys.stderr.write(str(e)+"\n")
        sys.exit(1)

    rp=pymetar.ReportParser()
    pr=rp.ParseReport(rep)

    print "Weather report for %s (%s) as of %s" %\
        (pr.getStationName(), station, pr.getISOTime())
    print "Values of \"None\" indicate that the value is missing from the report."
    print "Temperature: %s C / %s F" %\
        (pr.getTemperatureCelsius(), pr.getTemperatureFahrenheit())
    if pr.getWindchill() and pr.getWindchillF():
            print "Wind chill: %.2f C / %.2f F" % (pr.getWindchill(), pr.getWindchillF())

    print "Rel. Humidity: %s%%" % (pr.getHumidity())
    if pr.getWindSpeed() is not None:
        print "Wind speed: %0.2f m/s (%i Bft, %0.2f knots)" % \
            (pr.getWindSpeed(), pr.getWindSpeedBeaufort(), pr.getWindSpeedKnots())
    else:
        print "Wind speed: None"
        
    print "Wind direction: %s deg (%s)" %\
        (pr.getWindDirection(), pr.getWindCompass())
    if pr.getPressure() is not None:
        print "Pressure: %s hPa" % (int(pr.getPressure()))
    else:
        print "Pressure: None"

    print "Dew Point: %s C / %s F" %\
        (pr.getDewPointCelsius(), pr.getDewPointFahrenheit())
    print "Weather:",pr.getWeather()
    print "Sky Conditions:",pr.getSkyConditions()



if __name__ == "__main__":
    get_weather()
