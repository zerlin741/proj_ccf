from absl import app, flags
import time
import functools
import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

FLAGS = flags.FLAGS

def longtime_add(x, y, run_time=40):
	print("pid: ", os.getpid(), "  ppid: ", os.getppid())
	time.sleep(run_time)
	return x+y

def multi_thread_add(x, y, max_workers=10):
	f = longtime_add
	func = functools.partial(f, x, y)
	with ThreadPoolExecutor(max_workers=max_workers) as executor:
		future_list = [
			executor.submit(func) for i in range(20)
		]
	result = []
	for future in future_list:
		result.append(future.result())
	return sum(result)

def multi_process_add(x, y, max_workers=10):
	f = longtime_add
	func = functools.partial(f, x, y)
	with ProcessPoolExecutor(max_workers=max_workers) as executor:
		future_list = [
			executor.submit(func) for i in range(20)
		]
	result = []
	for future in future_list:
		result.append(future.result())
	return sum(result)

def train_model(x, y):
	from coin_trade.Strategy.random_forest_classifier.model import TradeableModel
	params = {
		'short_n': 2,
		'long_n': 24,
	}
	model = TradeableModel(exchange='Okex', symbol='BTC-USDT', kline_period='1h', params=params)
	model.train(grid_search=True)

def main(_):
	func_map = {
		'longtime_add': longtime_add,
		'multi_thread_add': multi_thread_add,
		'multi_process_add': multi_process_add,
		'train_model': train_model
	}
	func_name = FLAGS.func_name
	func = func_map.get(func_name)
	assert func is not None, "Invalid function name"
	print('start at ', time.time())
	print(func(x=FLAGS.x, y=FLAGS.y))
	print('end at ', time.time())


if __name__ == '__main__':
	flags.DEFINE_string(
		'func_name',
		None,
		'name of function to call'
	)
	flags.DEFINE_float(
		'x',
		None,
		'x'
	)
	flags.DEFINE_float(
		'y',
		None,
		'y'
	)
	app.run(main)
