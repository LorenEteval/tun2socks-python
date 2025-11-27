#include <string>
#if defined _WIN64
    #define _hypot hypot
    #include <cmath>
#endif
#include <pybind11/pybind11.h>

#include "tun2socks.h"

namespace py = pybind11;

namespace {
    void startFromArgs(const std::string &device, const std::string &networkInterface,
                       const std::string &logLevel, const std::string &proxy, const std::string &restAPI,
                       const std::string &tcpSendBufferSize = "",
                       const std::string &tcpReceiveBufferSize = "",
                       const bool tcpAutoTuning = false)
    {
        const GoString deviceString{device.data(), static_cast<ptrdiff_t>(device.size())};
        const GoString networkInterfaceString{networkInterface.data(), static_cast<ptrdiff_t>(networkInterface.size())};
        const GoString logLevelString{logLevel.data(), static_cast<ptrdiff_t>(logLevel.size())};
        const GoString proxyString{proxy.data(), static_cast<ptrdiff_t>(proxy.size())};
        const GoString restAPIString{restAPI.data(), static_cast<ptrdiff_t>(restAPI.size())};
        const GoString tcpSendBufferSizeString{
            tcpSendBufferSize.data(), static_cast<ptrdiff_t>(tcpSendBufferSize.size())
        };
        const GoString tcpReceiveBufferSizeString{
            tcpReceiveBufferSize.data(), static_cast<ptrdiff_t>(tcpReceiveBufferSize.size())
        };
        const GoUint8 tcpAutoTuningBool{static_cast<GoUint8>(tcpAutoTuning)};

        {
            py::gil_scoped_release release;

            ::startFromArgs(deviceString, networkInterfaceString,
                            logLevelString, proxyString, restAPIString,
                            tcpSendBufferSizeString,
                            tcpReceiveBufferSizeString,
                            tcpAutoTuningBool);

            py::gil_scoped_acquire acquire;
        }
    }

    PYBIND11_MODULE(tun2socks, m)
    {
        m.def("startFromArgs",
              &startFromArgs,
              "Start tun2socks with custom arguments",
              py::arg("device"), py::arg("networkInterface"),
              py::arg("logLevel"), py::arg("proxy"), py::arg("restAPI"),
              py::arg("tcpSendBufferSize") = "",
              py::arg("tcpReceiveBufferSize") = "",
              py::arg("tcpAutoTuning") = false);

        m.attr("__version__") = "2.6.0.1";
    }
}
