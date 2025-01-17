#!/usr/bin/env -S uv run -q

# Uses maxmind.com databases (free)
import geoip2.database

# This is super sloppy, sorry. You should know how to Python in order to use
# this. Feel free to bug me in the usual spots if you have a question.
with (
    geoip2.database.Reader('./GeoLite2-City.mmdb') as city_reader,
    geoip2.database.Reader('./GeoLite2-ASN.mmdb') as asn_reader,
    open("ips.txt") as f
):
    for line in f:
        ip = line.strip()
        try:
            cr = city_reader.city(ip)
            ar = asn_reader.asn(ip)
            print(f"{ip},{ar.autonomous_system_number},{ar.autonomous_system_organization},{cr.city.name},"
                  f"{cr.subdivisions.most_specific.name},{cr.country.iso_code}")
        except geoip2.errors.AddressNotFoundError:
            print(f"{ip}: Unknown")
