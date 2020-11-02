#include "matrix_prepared_alert.h"

std::string MatrixPreparedAlert::getText() const {
  return text_;
}

MatrixPreparedAlert::MatrixPreparedAlert(const std::string &text) : text_(text) {

}