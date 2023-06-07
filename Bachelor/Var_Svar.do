*Time-Serie
generate trimestre = tq(2003q1)+_n-1
format trimestre %tq
tsset trimestre

*Diff in logs de GDP et Diff des autres vars
gen l_GDP = ln(GDP)
gen g_GDP = d.l_GDP
gen d_Commodities = D.Commodities
gen d_CPI = d.CPI
gen g_CPI = d_CPI/CPI[_n-1] * 100
gen d_FedRate = d.FedRate
gen g_Commodities = d_Commodities/Commodities[_n-1] * 100
replace g_GDP = g_GDP * 100
gen TxGDPAbsolu = .
replace TxGDPAbsolu = g_GDP if g_GDP >= 0
replace TxGDPAbsolu = g_GDP * -1 if g_GDP < 0


*Graph
twoway (line GDP trimestre)	
twoway (line FedRate trimestre)	
twoway (line Commodities trimestre)
twoway (line CPI trimestre)

twoway (line g_CPI trimestre)	
twoway (line g_GDP trimestre)	
twoway (line g_Commodities trimestre)	
twoway (line d_FedRate trimestre)	

*Graph pour présentation

gen recession = r(max)*4 if g_GDP > 0
replace recession = r(min)*3 if g_GDP < 0
twoway (area recession trimestre, color(gs14)) (tsline g_Commodities, lcolor (blue))


*Test de Stationnarité des Variables -> Oui
foreach var of varlist g_GDP g_CPI g_Commodities d_FedRate {
    dfuller `var'
}

foreach var of varlist g_GDP g_CPI g_Commodities d_FedRate {
    pperron `var'
}

*Regression + Nombre de lags opti 
varsoc g_GDP g_Commodities d_FedRate g_CPI, maxlag(10)
var g_GDP g_Commodities d_FedRate g_CPI, lags(1)

*Diagnostic
varstable 
vargranger

*IRF 
irf set irf
irf create IRF1, replace  step(8)
irf graph irf, xlabel(0(2)8) irf(IRF1) yline(0,lcolor(black)) byopts(yrescale)

*Decomposition de la Variance
irf table fevd, irf(IRF1) impulse(g_GDP g_Commodities d_FedRate g_CPI) response(g_GDP) noci


*SVAR
matrix A = (1,0,0,0 \ .,1,0,0 \ .,.,1,0 \ .,.,.,1)
matrix B = (.,0,0,0 \ 0,.,0,0 \ 0,0,.,0 \ 0,0,0,.)
svar g_GDP g_CPI d_FedRate g_Commodities, lags(5) aeq(A) beq(B)

*Matrice A & B
matlist e(A)
matlist e(B)

*SIRF
irf create order1, set(var2.irf) replace step(8)
irf graph sirf, xlabel(0(2)8) irf(order1) yline(0,lcolor(black)) byopts(yrescale)

*Decomposition de la Variance
irf table fevd, irf(order1) impulse(g_GDP g_Commodities d_FedRate g_CPI) response(g_GDP) noci

*Matrice Cholesky (Pas très Utile..)
matrix chol=e(Sigma)
matrix chol2=cholesky(chol)
matrix list chol2

