#pragma once

#include <memory>
#include <string>

#include "alert.pb.h"

class PreparedAlert{}; // virtual -> TelegramPreparedAlert, MatrixPreparedAlert...

class Sender {
public:
    virtual void send(std::shared_ptr<PreparedAlert> prepared_alert) = 0;
};

class Preparer {
public:
    virtual std::shared_ptr<PreparedAlert> prepare(const alert::Alert& alert) const = 0;
};

class Factory {
public:
    virtual std::shared_ptr<Sender> createSender(const std::string& chat_id) const = 0;
    virtual std::shared_ptr<Preparer> createPreparer() const = 0;
};
