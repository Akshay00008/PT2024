from .etl import gatherData
from .api import login, summaryPageData, senarioPlannerData,fg_item ,alternateEntangled, updateDocuments, forecastAll, forecastplanner_code, deficient, forecastSearch, subassemblyInitial, subassemblyFinal, saveSnap, saveFilter, getFilter, getProductCode, getSnapFG, getSnapScenario, addUser, update, delete, getUsers, export_forecasting, plannercode
from flask import Blueprint
from ..utilities.subAssemblyHierarchy import createHierarchy

routes = Blueprint('routes' ,__name__)

routes.route('/run/ETL', methods = ['POST', 'GET'])(gatherData)
routes.route('/login', methods = ['POST', 'GET'])(login)
routes.route('/<location>/summarypage/<dateRange>', methods = ['POST', 'GET'])(summaryPageData)
# routes.route('/<location>/scenerioplanner/<pageNumber>', methods = ['POST', 'GET'])(senarioPlannerData)
routes.route('/<location>/scenerioplanner', methods = ['POST', 'GET'])(senarioPlannerData)
routes.route('/<location>/alternate-entangled/<user>', methods = ['POST', 'GET'])(alternateEntangled)
routes.route('/<location>/updateQOH/<user>', methods = ['POST', 'GET'])(updateDocuments)
routes.route('/<location>/forecastCompleteV2/<int:page_number>/<int:page_size>', methods = ['POST', 'GET'])(forecastAll)
routes.route('/<location>/forecastSearchV2/<searchVal>', methods = ['POST', 'GET'])(forecastSearch)
routes.route('/<location>/subassembly/<parent>/<child>', methods = ['POST', 'GET'])(subassemblyInitial)
routes.route('/<location>/subassemblyV2/<parent>/<child>', methods = ['POST', 'GET'])(subassemblyFinal)
routes.route('/<location>/save-snap/<user>', methods = ['POST', 'GET'])(saveSnap)
routes.route('/<location>/save-filter/<user>', methods = ['POST', 'GET'])(saveFilter)
routes.route('/<location>/get-filter/<user>', methods = ['POST', 'GET'])(getFilter)
routes.route('/<location>/get-productCode', methods = ['POST', 'GET'])(getProductCode)
routes.route('/<location>/get-snap-FG/<user>', methods = ['GET', 'POST'])(getSnapFG)
routes.route('/<location>/get-snap-scenarios/<user>/<fg>', methods = ['GET', 'POST'])(getSnapScenario)
routes.route('/<location>/createHierarchy', methods = ['GET', 'POST'])(createHierarchy)
routes.route('/add-user', methods = ['GET', 'POST'])(addUser)
routes.route('/update-user', methods = ['GET', 'POST'])(update)
routes.route('/delete-user', methods = ['GET', 'POST'])(delete)
routes.route('/get-user', methods = ['GET', 'POST'])(getUsers)
routes.route('/<location>/get-plannercode', methods = ['POST', 'GET'])(plannercode)
routes.route('/<location>/export-forecasting', methods = ['GET', 'POST'])(export_forecasting)
routes.route('/<location>/forecastplan_codeV2/<int:page_number>/<int:page_size>', methods = ['POST', 'GET'])(forecastplanner_code)
routes.route('/<location>/forecastdeficientV2/<int:page_number>/<int:page_size>/<val>', methods = ['POST', 'GET'])(deficient)
routes.route('/<location>/fg_item', methods = ['GET', 'POST'])(fg_item)

