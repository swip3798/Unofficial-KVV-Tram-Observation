import kvvapi
import tqdm
from multiprocessing import Pool
import json
import sys




def main(city_id, range_count, start_count = 0):
	possible_ids = []	
	results=[]
	for i in range(start_count, range_count, 1):
		possible_ids.append("de:" + city_id + ":" + str(i))
	for i in possible_ids:
		print(i)
	'''
	pool = Pool(threads)
	print("Start pinging...", len(possible_ids))
	for _ in tqdm.tqdm(pool.imap_unordered(kvvapi.get_stop_by_id, possible_ids), total=len(possible_ids)):
	    results.append(_)
	pool.close()
	'''
	pbar = tqdm.tqdm(possible_ids)
	for i in pbar:
		response = kvvapi.get_stop_by_id(i)
		try:
			if response != None:
				results.append(response)
				dick = []
				for i in results:
					dick.append({"stop_id":i.stop_id, "name":i.name, "lat":i.lat, "lon":i.lon})
				with open("db/" + city_id + "_" + str(start_count) + "_" + str(range_count) + ".json", "w") as f:
					f.write(json.dumps(dick, indent = 4, sort_keys=True))
		except (KeyboardInterrupt, SystemExit):
			dick = []
			for i in results:
				dick.append({"stop_id":i.stop_id, "name":i.name, "lat":i.lat, "lon":i.lon})
				with open("db/" + city_id + "_" + str(start_count) + "_" + str(range_count) + ".json", "w") as f:
					f.write(json.dumps(dick, indent = 4, sort_keys=True))
			exit()
	pbar.close()
	

	

if __name__ == '__main__':
	if len(sys.argv) == 3:
		main(sys.argv[1], int(sys.argv[2]))
	elif len(sys.argv) == 4:
		main(sys.argv[1], int(sys.argv[3]), int(sys.argv[2]))
	else:
		main(input("city_id: "), int(input("Range: ")))