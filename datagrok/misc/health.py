'''Various utilities for health and fitness.

Some data from http://www.runnersworld.com/article/0,7120,s6-242-304-311-8402-0,00.html

'''

# harris-benedict factor: coefficent of bmr, estimates daily calorie burn
hbf = {
    'sedentary': 1.2, # little or no exercise
    'light': 1.375,   # light exercise/sports 1-3 days/week
    'moderate': 1.55, # moderate exercise/sports 3-5 days/week
    'very': 1.725,    # hard exercise/sports 6-7 days a week
    'extra': 1.9,     # very hard exercise/sports & physical job or 2x training
}

# Human needs to burn about 3500 calories to lose one pound.
calories_per_pound = 3500

pounds_per_kilogram = 0.45359237

# net calorie burn = ncb factor * weight (lb). Net calorie burn does not
# include basal metabolism.
ncbfactor_running = .53
ncbfactor_walking = .30

# total calorie burn = tcb factor * weight (lb). Total calorie burn includes
# basal metabolism.
tcbfactor_running = .75
tcbfactor_walking = .53


def targetheartrate(age):
    '''Returns a tuple of target heart rates:
        (low, high, max)
    
    '''
    mhr = 220 - int(age)
    return (int(mhr * .50), int(mhr * .85), mhr)


def karvonen_heartrate(age, rhr):
    '''Returns a tuple of heart rates given age and resting heart rate (rhr)
    based on the Karvonen equation:

        (resting, fat burn, cardio, maximum)
 
    '''
    mhr = 206.9 - (0.67 * age)
    hrrange = mhr - rhr
    return (
        int(rhr), # resting
        int(hrrange * .65 + rhr), # fat burn
        int(hrrange * .85 + rhr), # cardio
        int(mhr)) # maximum


def bmr(male, age, wt, ht, metric=False,
        _coeffs = {
            # male, metric
            (True, False): (66, 6.23, 12.7, 6.8),
            (False, False): (655, 4.35, 4.7, 4.7),
            (True, True): (66, 13.7, 5, 6.8),
            (False, True): (655, 9.6, 1.8, 4.7),
        }):
    '''Calculate basal metabolic rate.

    male - True or False
    age - age in years
    if metric is False or omitted:
        wt - weight in pounds
        ht - height in inches
    if metric is True:
        wt - weight in kg
        ht - height in cm

    '''
    (c, w, h, a) = _coeffs[(male, bool(metric))]
    return c + w*wt + h*ht - a*age


def bmi(wt, ht, metric=False,
        _coeffs = {
            True: 703,
            False: 1,
        }):
    '''Calculate the body mass index.
    
    if english is True or omitted:
        wt - weight in pounds
        ht - height in inches
    if english is False:
        wt - weight in kg
        ht - height in meters
    '''
    return wt / ht / ht * _coeffs[bool(metric)]


