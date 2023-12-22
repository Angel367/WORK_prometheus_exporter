import (
    "net/http"
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promhttp"
)

var (
    httpDuration = prometheus.NewHistogramVec(
        prometheus.HistogramOpts{
            Name: "http_request_duration_seconds",
            Help: "HTTP request duration in seconds.",
        },
        []string{"handler", "status"},
    )
)

func init() {
    prometheus.MustRegister(httpDuration)
}

func handler(w http.ResponseWriter, r *http.Request) {
    start := time.Now()

    // Your HTTP handler logic here

    duration := time.Since(start).Seconds()
    httpDuration.WithLabelValues("new_handler", strconv.Itoa(http.StatusOK)).Observe(duration)
}

func main() {
    http.Handle("/metrics", promhttp.Handler())
    http.HandleFunc("https://moy-zakupki.ru/", handler)
    http.ListenAndServe(":8080", nil)
}
