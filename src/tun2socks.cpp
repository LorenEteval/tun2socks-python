#include <string>
#if defined _WIN64
    #define _hypot hypot
    #include <cmath>
#endif
#include <pybind11/pybind11.h>

#include "tun2socks.h"

namespace py = pybind11;

namespace {
    void startFromArgs(const std::string &device, const std::string &networkInterface, const std::string &logLevel,
        const std::string &proxy, const std::string &restAPI)
    {
        GoString deviceString{device.data(), static_cast<ptrdiff_t>(device.size())};
        GoString networkInterfaceString{networkInterface.data(), static_cast<ptrdiff_t>(networkInterface.size())};
        GoString logLevelString{logLevel.data(), static_cast<ptrdiff_t>(logLevel.size())};
        GoString proxyString{proxy.data(), static_cast<ptrdiff_t>(proxy.size())};
        GoString restAPIString{restAPI.data(), static_cast<ptrdiff_t>(restAPI.size())};

        {
            py::gil_scoped_release release;

            ::startFromArgs(deviceString, networkInterfaceString, logLevelString, proxyString, restAPIString);

            py::gil_scoped_acquire acquire;
        }
    }

    PYBIND11_MODULE(tun2socks, m)
    {
        m.def("startFromArgs",
            &startFromArgs,
            "Start tun2socks with custom arguments",
            py::arg("device"), py::arg("networkInterface"), py::arg("logLevel"), py::arg("proxy"), py::arg("restAPI"));

        m.attr("__version__") = "2.5.2.1";
    }
}
