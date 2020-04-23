package com.storefront.respository;

import com.storefront.model.CustomerCases;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface PALSUsersRepository extends MongoRepository<PALSUsers, String> {

}