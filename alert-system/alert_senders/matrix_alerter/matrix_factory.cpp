#include <memory>

#include "matrix_factory.h"
#include "matrix_preparer.h"
#include "matrix_sender.h"

MatrixFactory::MatrixFactory() {}

std::shared_ptr<Sender> MatrixFactory::createSender(const std::string &chat_id) const {
  return std::make_shared<MatrixSender>(chat_id);
}

std::shared_ptr<Preparer> MatrixFactory::createPreparer() const {
  return std::make_shared<MatrixPreparer>();
}
