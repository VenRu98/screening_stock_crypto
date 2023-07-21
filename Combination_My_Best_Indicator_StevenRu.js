//@version=5
indicator(title="Combination Indicator And Screening StevenRu", shorttitle="Combination VenRu", overlay=true, timeframe="", timeframe_gaps=true)

// ================================================================================================= //
// ================================================================================================= //
// =================== INDICATOR VEN RU START ====================================================== //
// ================================================================================================= //
// ================================================================================================= //

// = Array = //
var highs = array.new_float(0)
var lows = array.new_float(0)

insidebar_pivot_parent = input(true, title="Insidebar Pivot Parent")
// ============ //
// = Function = //
// ============ //
fractal(n,candle, note) =>
    bool flagDownFrontier = true
    bool flagUpFrontier0 = true
    bool flagUpFrontier1 = true
    bool flagUpFrontier2 = true
    bool flagUpFrontier3 = true
    bool flagUpFrontier4 = true
    if note == "high"
        for i = 1 to n
            flagDownFrontier := flagDownFrontier and (candle[n-i] < candle[n])
            flagUpFrontier0 := flagUpFrontier0 and (candle[n+i] < candle[n])
            flagUpFrontier1 := flagUpFrontier1 and (candle[n+1] <= candle[n] and candle[n+i + 1] < candle[n])
            flagUpFrontier2 := flagUpFrontier2 and (candle[n+1] <= candle[n] and candle[n+2] <= candle[n] and candle[n+i + 2] < candle[n])
            flagUpFrontier3 := flagUpFrontier3 and (candle[n+1] <= candle[n] and candle[n+2] <= candle[n] and candle[n+3] <= candle[n] and candle[n+i + 3] < candle[n])
            flagUpFrontier4 := flagUpFrontier4 and (candle[n+1] <= candle[n] and candle[n+2] <= candle[n] and candle[n+3] <= candle[n] and candle[n+4] <= candle[n] and candle[n+i + 4] < candle[n])
    else if note == "low"
        for i = 1 to n
            flagDownFrontier := flagDownFrontier and (candle[n-i] > candle[n])
            flagUpFrontier0 := flagUpFrontier0 and (candle[n+i] > candle[n])
            flagUpFrontier1 := flagUpFrontier1 and (candle[n+1] >= candle[n] and candle[n+i + 1] > candle[n])
            flagUpFrontier2 := flagUpFrontier2 and (candle[n+1] >= candle[n] and candle[n+2] >= candle[n] and candle[n+i + 2] > candle[n])
            flagUpFrontier3 := flagUpFrontier3 and (candle[n+1] >= candle[n] and candle[n+2] >= candle[n] and candle[n+3] >= candle[n] and candle[n+i + 3] > candle[n])
            flagUpFrontier4 := flagUpFrontier4 and (candle[n+1] >= candle[n] and candle[n+2] >= candle[n] and candle[n+3] >= candle[n] and candle[n+4] >= candle[n] and candle[n+i + 4] > candle[n])
    flagFrontier = flagUpFrontier0 or flagUpFrontier1 or flagUpFrontier2 or flagUpFrontier3 or flagUpFrontier4
    (flagDownFrontier and flagFrontier)

arr_is_not_empty(highs, lows)=>
    array.size(highs) > 0 and array.size(lows) > 0

check_inside_bar(prev_high,prev_low) =>
    close <= prev_high and close >= prev_low and open >= prev_low and open <= prev_high
    // high <= prev_high and low >= prev_low

isInside() =>
    last_high = 0.0
    last_low = 0.0
    previousBar = 1
    isInsidePattern = check_inside_bar(high[previousBar], low[previousBar])
    result = false

    // Check previous inside barcolor    
    if( arr_is_not_empty(highs, lows) )
        get_high_from_array = array.get(highs,0)
        get_low_from_array = array.get(lows,0)

        // if not breakout or inside bar
        if( check_inside_bar(get_high_from_array, get_low_from_array) )
            result := true
        // else breakout
        else 
            last_high = array.get(highs,0)
            last_low = array.get(lows,0)
            array.pop(highs)
            array.pop(lows)

    else
        if (isInsidePattern)
            if(insidebar_pivot_parent)
                array.push(highs, high[1] )
                array.push(lows, low[1] )
            else
                array.push(highs, high )
                array.push(lows, low )
            result := true

    [result, last_high, last_low]

smma(src, length) =>
    smma =  0.0
    smma := na(smma[1]) ? ta.sma(src, length) : (smma[1] * (length - 1) + src) / length
    smma


src = close
out_0 = ta.ema(src, 5)

out_H4 = ta.ema(src,13)
out_H4_H1 = ta.ema(src,21)
out_H4_H1_M15_34 = ta.ema(src,34)
out_H4_H1_M15_55 = ta.ema(src,55)

out_ema_1 = (timeframe.period == "60" ? out_H4_H1           : (timeframe.period == "15" ? out_H4_H1_M15_34  : out_H4))
out_ema_2 = (timeframe.period == "60" ? out_H4_H1_M15_34    : (timeframe.period == "15" ? out_H4_H1_M15_55  : out_H4_H1))

// ========== //
// Inside Bar //
// ========== //
[result_insidebar, last_high, last_low] = isInside()
confirm_breakout = result_insidebar[1] and not result_insidebar and result_insidebar[2]
insidebar_bull_breakout = confirm_breakout and open < close and close > out_0
insidebar_bear_breakout = confirm_breakout and open > close and close < out_0

// ================ //
// == Alligator == //
// ================ //
lipsLength = input.int(3, minval=1, title="Lips Length (Alligator)")
lipsOffset = input.int(2, title="Lips Offset (Alligator)")
lips = smma(hl2, lipsLength)

alligator_bull_breakout = high >= lips[lipsOffset]
alligator_bear_breakout = low <= lips[lipsOffset]

// ================ //
// == Stochastic == //
// ================ //
periodK = input.int(5, minval=1, title="Period (Stochastic)")
smoothK = input.int(3, minval=1, title="K (Stochastic)")
periodD = input.int(3, minval=1, title="D (Stochastic)")
k = ta.sma(ta.stoch(close, high, low, periodK), smoothK)
d = ta.sma(k, periodD)

stochastic_bull_potential = k > d
stochastic_bear_potential = k < d

// ========== //
// == MACD == //
// ========== //
fast_length = input.int(12, minval=1, title="Fast (MACD)")
slow_length = input.int(26, minval=1, title="Slow (MACD)")
signal_length = input.int(9, minval=1, title="Signal (MACD)")
sma_source = "EMA"
fast_ma = ta.ema(src, fast_length)
slow_ma = ta.ema(src, slow_length)
macd = fast_ma - slow_ma
signal = ta.ema(macd, signal_length)
hist = macd - signal
histogram_status = hist>=0 ? (hist[1] < hist ? "Summer" : "Autumn") : (hist[1] < hist ? "Spring" : "Winter") 
// Signal MACD //
macd_bull_breakout_potential = (histogram_status == "Summer" or histogram_status == "Spring" ) and macd[1] < macd
macd_bear_breakout_potential = (histogram_status == "Winter" or histogram_status == "Autumn" ) and macd[1] > macd

// ======== //
// == AO == //
// ======== //
ao = ta.sma(hl2,5) - ta.sma(hl2,34)
get_ao = ta.change(ao) <= 0 ? "red" : "green"
ao_bull_potential = get_ao == "green" or get_ao[1] == "green"
ao_bear_potential = get_ao == "red" or get_ao[1] == "red"

// ========== //
// == OBV === //
// ========== //
obv = ta.cum(math.sign(ta.change(src)) * volume)
// Signal OBV //
obv_bull_breakout_potential = obv > obv[2] and obv > obv[1] and close > open
obv_bear_breakout_potential = obv < obv[2] and obv < obv[1] and close < open

//=====//
// SAR //
//=====//
start = 0.055
increment = 0.055
maximum = 0.55
out_sar = ta.sar(start, increment, maximum)
sar_bull_potential = out_sar < close
sar_bear_potential = out_sar > close

// =================== //
// == EMA Smoothing == //
// =================== //
len = 1
src_ema_smooth = close
out = ta.ema(src_ema_smooth, len)

smoothingLine = ta.sma(out, 5)

// ======== //
// == BB == //
// ======== //
length_bb = (timeframe.period == "60" ? 34    : (timeframe.period == "15" ? 55  : 21))
src_bb = out
mult_bb = 2.0
basis_bb = ta.sma(src_bb, length_bb)
dev_bb = mult_bb * ta.stdev(src_bb, length_bb)
upper_bb = basis_bb + dev_bb
lower_bb = basis_bb - dev_bb

bb_bull_potential = basis_bb < smoothingLine
bb_bear_potential = basis_bb > smoothingLine

// ======== DRAW ========= //
// Signal Momentum
bull_potential_indicator_venru = macd_bull_breakout_potential and obv_bull_breakout_potential and ao_bull_potential and not result_insidebar and stochastic_bull_potential and alligator_bull_breakout and sar_bull_potential and bb_bull_potential
bear_potential_indicator_venru = macd_bear_breakout_potential and obv_bear_breakout_potential and ao_bear_potential and not result_insidebar and stochastic_bear_potential and alligator_bear_breakout and sar_bear_potential and bb_bear_potential

// ================================================================================================= //
// ================================================================================================= //
// =================== SCREENING VEN RU START ====================================================== //
// ================================================================================================= //
// ================================================================================================= //

//=========//
// OVERLAY //
//=========//

//=====//
// EMA //
//=====//

out_5 = ta.ema(src, 5)
out_10 = ta.ema(src, 10)

ema_bull_potential = out_5 < close and out_10 < close
ema_bear_potential = out_5 > close and out_10 > close

//=====//
// HMA //
//=====//
length = 9
hullma = ta.wma(2*ta.wma(src, length/2)-ta.wma(src, length), math.floor(math.sqrt(length)))

hma_bull_potential = hullma < close
hma_bear_potential = hullma > close

//======//
// VWAP //
//======//
var cumVol = 0.
cumVol += nz(volume)
if barstate.islast and cumVol == 0
    runtime.error("No volume is provided by the data vendor.")
    
computeVWAP(src, isNewPeriod, stDevMultiplier) =>
    var float sumSrcVol = na
    var float sumVol = na
    var float sumSrcSrcVol = na
    sumSrcVol := isNewPeriod ? src * volume : src * volume + sumSrcVol[1]
    sumVol := isNewPeriod ? volume : volume + sumVol[1]
    sumSrcSrcVol := isNewPeriod ? volume * math.pow(src, 2) : volume * math.pow(src, 2) + sumSrcSrcVol[1]
    _vwap = sumSrcVol / sumVol
    variance = sumSrcSrcVol / sumVol - math.pow(_vwap, 2)
    variance := variance < 0 ? 0 : variance
    stDev = math.sqrt(variance)
    lowerBand = _vwap - stDev * stDevMultiplier
    upperBand = _vwap + stDev * stDevMultiplier
    [_vwap, lowerBand, upperBand]

hideonDWM = false
var anchor = "Session"
src_vwap = hlc3

showBands = true
stdevMult = 1.0

timeChange(period) =>
    ta.change(time(period))

isNewPeriod = switch anchor
    "Session" => timeChange("D")
    => false

isEsdAnchor = anchor == "Earnings" or anchor == "Dividends" or anchor == "Splits"
if na(src_vwap[1]) and not isEsdAnchor
    isNewPeriod := true

float vwapValue = na

if not (hideonDWM and timeframe.isdwm)
    [_vwap, bottom, top] = computeVWAP(src_vwap, isNewPeriod, stdevMult)
    vwapValue := _vwap

vwap_bull_potential = vwapValue < close
vwap_bear_potential = vwapValue > close

//======//
// VWMA //
//======//
len_vwma = 20
vwmaValue = ta.vwma(src, len_vwma)
vwma_bull_potential = high > vwmaValue
vwma_bear_potential = low < vwmaValue

//============//
// OSCILLATOR //
//============//
    
//=====//
// RSI //
//=====//
up_7 = ta.rma(math.max(ta.change(src), 0), 7)
down_7 = ta.rma(-math.min(ta.change(src), 0), 7)

up_14 = ta.rma(math.max(ta.change(src), 0), 14)
down_14 = ta.rma(-math.min(ta.change(src), 0), 14)

rsi_7 = down_7 == 0 ? 100 : up_7 == 0 ? 0 : 100 - (100 / (1 + up_7 / down_7))

rsi_14 = down_14 == 0 ? 100 : up_14 == 0 ? 0 : 100 - (100 / (1 + up_14 / down_14))

rsi_bull_potential = rsi_7 > 30 and rsi_14 > 30
rsi_bear_potential = rsi_7 < 70 and rsi_14 < 70


//============//
// STOCHASTIC //
//============//
smoothK_screening = 3
smoothD_screening = 3
lengthRSI = 14
lengthStoch = 14

k_stoch = ta.sma(ta.stoch(close, high, low, lengthStoch), smoothK_screening)
d_stoch = ta.sma(k_stoch, smoothD_screening)

rsi1 = ta.rsi(close, lengthRSI)
k_stoch_rsi = ta.sma(ta.stoch(rsi1, rsi1, rsi1, lengthStoch), smoothK_screening)
d_stoch_rsi = ta.sma(k_stoch_rsi, smoothD_screening)

stochastic_bull_potential_screening = d_stoch > 20 and k_stoch > 20 and k_stoch_rsi > 20 and d_stoch_rsi > 20
stochastic_bear_potential_screening = d_stoch < 80 and k_stoch < 80 and k_stoch_rsi < 80 and d_stoch_rsi < 80

//========================//
// Williams Percent Range //
//========================//
length_WPR = 14
_pr(length) =>
    max = ta.highest(length)
    min = ta.lowest(length)
    100 * (src - max) / (max - min)
percentR = _pr(length_WPR)

wpr_bull_potential = percentR > -80
wpr_bear_potential = percentR < -20

//=====//
// CCI //
//=====//
length_cci = 20
src_cci = hlc3
ma = ta.sma(src_cci, length_cci)
cci = (src_cci - ma) / (0.015 * ta.dev(src_cci, length_cci))
cci_bull_potential = cci >= -100
cci_bear_potential = cci <= 100

// Proces.... //
// Proces.... //
// Proces.... //
//    ....    //

bull_potential_screening_venru =  close > open and wpr_bull_potential and ema_bull_potential and hma_bull_potential and vwma_bull_potential and vwap_bull_potential and rsi_bull_potential and stochastic_bull_potential_screening and cci_bull_potential
bear_potential_screening_venru =  close < open and wpr_bear_potential and ema_bear_potential and hma_bear_potential and vwma_bear_potential and vwap_bear_potential and rsi_bear_potential and stochastic_bear_potential_screening and cci_bear_potential

bull_potential = bull_potential_indicator_venru and bull_potential_screening_venru
bear_potential = bear_potential_indicator_venru and bear_potential_screening_venru

show_5_newest_momentum = input(true, title="Show Newest Momentum")

bgcolor(bull_potential? color.green : na, transp=40)
bgcolor(bear_potential? color.red : na, transp=40)

bgcolor(show_5_newest_momentum ? color.rgb(20,24,35) : na, transp=70, offset=-10)
