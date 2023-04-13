# Handige Queries

## Join de het flight met de meest recenste data (old)

```sql
select f.*, d1.datetime_scraped, d1.number_seats_available, d1.ticket_price, d1.datetime_depart, d1.datetime_arrival
from flights f
join flight_data d1 on d1.flight_key_id = f.flight_key
left outer join flight_data d2 on (f.flight_key = d2.flight_key_id and
	(d1.datetime_scraped < d2.datetime_scraped or (d1.datetime_scraped = d2.datetime_scraped and d1.datetime_scraped < d2.datetime_scraped)))
where d2.flight_key_id is null;
```