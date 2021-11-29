from utils import rf_counter

all_flights = rf_counter.MultipleFlights(verbose=True)

all_flights.g_exc_curve(save_figure=False)

# input('Press ENTER to close...')
