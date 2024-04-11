#include "libCacheSim.h"

/* open trace, see quickstart_lib.md for opening csv and binary trace */
reader_t *reader = open_trace("../data/trace.vscsi", VSCSI_TRACE, NULL);

/* craete a container for reading from trace */
request_t *req = new_request();

/* create a LRU cache */
common_cache_params_t cc_params = {.cache_size=1024*1024U}; 
cache_t *cache = LRU_init(cc_params, NULL); 

/* counters */
uint64_t req_byte = 0, miss_byte = 0;
uint64_t n_req = 0, n_miss = 0;

/* loop through the trace */
while (read_one_req(reader, req) == 0) {
    if (cache->get(cache, req) == cache_ck_miss) {
        miss_byte += req->obj_size;
        n_miss++;
    }
    req_byte += req->obj_size; 
    n_req++;
}

printf("miss ratio: %.4lf, byte miss ratio %.4lf\n", 
        (double)n_miss / n_req, (double)miss_byte / req_byte);

/* cleaning */
close_trace(reader);
free_request(req);
cache->cache_free(cache);
